from src.settings.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # admin, medico, tecnico
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    # relacionamento
    exames = db.relationship("EcgExam", backref="usuario", lazy=True)

    def __init__(self, nome, email, senha, tipo="tecnico"):
        self.nome = nome
        self.email = email
        self.senha_hash = senha #generate_password_hash(senha)
        self.tipo = tipo

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f"<Usuario {self.nome}>"