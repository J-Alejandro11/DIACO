from src.models.reporte_quejas_model import ReporteQuejasManager
from src.database.conexionbd import db

class ReporteQuejasController:
    def __init__(self):
        self.manager = ReporteQuejasManager(db.session)

    def obtener_reporte_quejas(self):
        return self.manager.obtener_reporte_quejas()
