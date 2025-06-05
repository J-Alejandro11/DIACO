from src.models.revision_quejas_model import QuejasDetalladasManager
from src.database.conexionbd import db

class QuejasDetalladasController:
    def __init__(self):
        self.manager = QuejasDetalladasManager(db.session)

    def obtener_quejas_detalladas(self):
        return self.manager.obtener_quejas_detalladas()