from src.settings.extensions import db
import enum
import datetime


class SexoEnum(enum.Enum):
    MASCULINO = "M"
    FEMININO = "F"


class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True)

    # Identificador vindo do XML (ex.: <patient><id>...</id>)
    external_id = db.Column(db.String(64), unique=True, nullable=True, index=True)

    # Nome vindo do XML (ex.: <patient><name>...</name>)
    nome = db.Column(db.String(255), nullable=False)

    # No XML geralmente não vem CPF -> deixe opcional
    cpf = db.Column(db.String(14), unique=True, nullable=True)

    # No XML pode vir idade, mas data_nascimento normalmente não vem
    # Deixe data_nascimento opcional e adicione idade
    data_nascimento = db.Column(db.Date, nullable=True)
    idade = db.Column(db.Integer, nullable=True)
    idade_unidade = db.Column(db.String(16), nullable=True)  # "Y"/"M"/"D" (ano/mês/dia) se vier

    sexo = db.Column(db.Enum(SexoEnum), nullable=True)  # nullable=True porque pode vir vazio/indefinido

    # Campos que você comentou que aparecem no XML
    setor = db.Column(db.String(128), nullable=True)       # <department>
    leito = db.Column(db.String(64), nullable=True)        # <bedNo>
    peso_kg = db.Column(db.Float, nullable=True)           # <weight>
    altura_cm = db.Column(db.Float, nullable=True)         # <height>

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    exames = db.relationship("EcgExam", back_populates="paciente", lazy=True)

    def __repr__(self):
        return f"<Paciente {self.nome}>"