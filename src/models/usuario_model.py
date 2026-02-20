from src.settings.extensions import db

class StatusLembre:
    pass


class Usuario(db.Model):
    
    __tablename__ = "usuario"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    
    def __init__(self, name, email, senha):
        self.name = name
        self.email = email
        self.senha = senha
        
    def __repr__(self):
        return f"Usuario: {self.name} - {self.email} - {self.senha}"