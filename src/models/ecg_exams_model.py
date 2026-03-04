from src.settings.extensions import db
import datetime


class EcgExam(db.Model):

    __tablename__ = 'ecg_exams'

    id = db.Column(db.Integer, primary_key=True)

    paciente_id = db.Column(
        db.Integer, db.ForeignKey('pacientes.id'), nullable=False
    )

    data_exame = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    frequencia_media = db.Column(db.Integer, nullable=False)

    arquivo = db.Column(db.String(255), nullable=False)

    observacoes = db.Column(db.Text, nullable=True)

    created_by = db.Column(
        db.Integer, db.ForeignKey('usuarios.id'), nullable=False
    )

    # RELACIONAMENTOS (muito importante 👇)

    paciente = db.relationship('Paciente', back_populates='exames')
    usuario = db.relationship('Usuario', back_populates='exames')

    def __repr__(self):
        return f'<ECG Exam {self.id} - Paciente {self.paciente_id}>'
