from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'Usuarios'
    id_usuario = Column(Integer, primary_key=True)
    usuario = Column(String(100), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)

class UsuarioManager:
    def __init__(self, session):
        self.session = session

    def autenticar(self, usuario, contrasena):
        """
        Devuelve el usuario si el usuario y la contraseña coinciden, None si no existe.
        Equivalente a: SELECT * FROM Usuarios WHERE usuario = ... AND contrasena = ...;
        """
        return self.session.query(Usuario).filter_by(usuario=usuario, contrasena=contrasena).first()
