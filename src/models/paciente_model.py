from src.settings.extensions import db
import enum
import datetime


class SexoEnum(enum.Enum):
    MASCULINO = "M"
    FEMININO = "F"


class Paciente(db.Model):

    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.Enum(SexoEnum), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    exames = db.relationship("EcgExam", backref="paciente", lazy=True)

    def __repr__(self):
        return f"<Paciente {self.nome}>"