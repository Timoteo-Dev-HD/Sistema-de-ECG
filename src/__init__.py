from flask import Flask
from .settings.config import Config
from .settings.extensions import db, migrate

from apscheduler.schedulers.background import BackgroundScheduler
from src.services.ecg_import_service import import_local_ecgs
from src.utils.ftp_sync import sync_ftp


def create_app():
    app = Flask(
        __name__,
        template_folder='views/templates',
        static_folder='views/static',
    )
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    # bootstrap.init_app(app)

    try:
        from src.models.usuario_model import Usuario
        from src.models.ecg_exams_model import EcgExam
        from src.models.paciente_model import Paciente

        from .routes import register_routes
        register_routes(app)

    except Exception:
        pass

    # ==============================
    # 🔥 INICIAR SCHEDULER AQUI
    # ==============================

    scheduler = BackgroundScheduler()

    def job():
        with app.app_context():
            try:
                sync_ftp()
                import_local_ecgs()
                print("✔ ECG Sync executado")
            except Exception as e:
                print("Erro no sync:", e)

    scheduler.add_job(job, "interval", seconds=10)
    scheduler.start()

    # evita duplicação quando debug=True
    if app.debug:
        scheduler.pause()
        scheduler.resume()

    return app