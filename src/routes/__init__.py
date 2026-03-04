from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    session,
    send_file,
    current_app    
)
import bcrypt
import os

from sqlalchemy.orm import joinedload

from src.utils.auth_util import login_required
from src.controllers.login_controller import LoginController

from src.services.ecg_import_service import import_local_ecgs
from src.utils.ftp_sync import sync_ftp
from src.utils.impressora_util import print_pdf_to_ip

from src.models.ecg_exams_model import EcgExam
from src.models.paciente_model import Paciente

web = Blueprint('web', __name__)

# ==========================
# LOGIN
# ==========================
@web.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        email = request.form.get('email')
        senha = request.form.get('senha')
        lembre_mim = request.form.get('check')

        login_obj = LoginController()

        usuario_valido = login_obj.verificar_usuario_db(email, senha)

        if usuario_valido:
            usuario = login_obj.exibir_usuario(email)

            session['user_nome'] = usuario.nome
            session['user_id'] = usuario.id
            session['tipo'] = usuario.tipo

            return redirect(url_for('web.home'))

        return render_template('login.html', erro='Login inválido')

    return render_template('login.html')


# ==========================
# LOGOUT
# ==========================
@web.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('web.login'))


# ==========================
# HOME
# ==========================
@web.route('/home')
@login_required
def home():
    if 'user_id' not in session:
        return redirect(url_for('web.login'))

    return render_template('home.html')


@web.route('/ecg/<int:exam_id>')
@login_required
def ecg_view(exam_id):

    exame = EcgExam.query.get_or_404(exam_id)

    return render_template('ecg_view.html', exam=exame)




@web.route("/sync-ecg")
def sync_ecg():
    sync_ftp()          # baixa do FTP
    import_local_ecgs() # importa no banco
    return {"status": "ok"}


@web.route("/ecg/pdf/<int:id>")
def view_pdf(id):
    exam = EcgExam.query.get_or_404(id)

    # pega raiz do projeto (um nível acima de src)
    project_root = os.path.abspath(os.path.join(current_app.root_path, ".."))

    file_path = os.path.join(project_root, "ecg_local", exam.arquivo)

    if not os.path.exists(file_path):
        return f"Arquivo não encontrado: {file_path}", 404

    return send_file(file_path)

@web.route("/pacientes")
@login_required
def listar_pacientes():
    patients = (
        Paciente.query
        .options(joinedload(Paciente.exames))
        .all()
    )

    return render_template("pacientes.html", patients=patients)


@web.route("/patient/<int:id>")
@login_required
def paciente_detail(id):
    patient = Paciente.query.get_or_404(id)
    exams = EcgExam.query.filter_by(paciente_id=id)\
        .order_by(EcgExam.data_exame.desc())\
        .all()
    return render_template(
        "paciente_detail.html",
        patient=patient,
        exams=exams
    )

@web.route("/ecg/print/<int:id>")
@login_required
def print_exam(id):
    exam = EcgExam.query.get_or_404(id)

    project_root = os.path.abspath(os.path.join(current_app.root_path, ".."))
    file_path = os.path.join(project_root, "ecg_local", exam.arquivo)

    if not os.path.exists(file_path):
        return "Arquivo não encontrado", 404

    try:
        print_pdf_to_ip("172.19.0.30", file_path)
        return {"status": "Enviado para impressora"}
    except Exception as e:
        return {"erro": str(e)}, 500

# ==========================
# REGISTRO DO BLUEPRINT
# ==========================
def register_routes(app):
    app.register_blueprint(web)
