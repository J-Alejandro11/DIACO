from src.models.usuario_model import UsuarioManager
from src.database.conexionbd import db

class UsuarioController:
    def __init__(self):
        self.manager = UsuarioManager(db.session)

    def autenticar(self, usuario, contrasena):
        return self.manager.autenticar(usuario, contrasena)
