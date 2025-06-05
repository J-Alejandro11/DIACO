from src.models.lista_comercios_model import ListaComerciosManager
from src.database.conexionbd import db

class ComerciosUbicacionesController:
    def __init__(self):
        self.manager = ListaComerciosManager(db.session)

    def obtener_lista_comercios(self):
        return self.manager.obtener_lista_comercios()
