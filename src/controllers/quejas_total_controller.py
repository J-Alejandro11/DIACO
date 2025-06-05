from src.models.quejas_total_model import QuejasTotalManager
from src.database.conexionbd import db

class QuejasTotalController:
    def __init__(self):
        self.manager = QuejasTotalManager(db.session)

    def total_quejas(self):
        return self.manager.total_quejas()

    def total_comercios_reportados(self):
        return self.manager.total_comercios_reportados()
