from src.settings.extensions import db
from src.models.usuario_model import Usuario

class LoginController:
    
    def verificar_usuario_db(self, email:str, senha:str) -> bool:
        buscar_usuario = db.session.query(Usuario).filter(Usuario.email == email and Usuario.senha == senha).first()
        
        if not buscar_usuario:
            return False
        
        return True
    
    def exibir_usuario(self, email:str) -> Usuario:
        usuario = db.session.query(Usuario).filter(
            Usuario.email == email
        )
        
        if not usuario:
            return None
        
        return usuario