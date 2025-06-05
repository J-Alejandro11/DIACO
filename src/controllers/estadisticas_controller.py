from src.models.estadisticas_model import EstadisticasManager
from src.database.conexionbd import db

class EstadisticasController:
    def __init__(self):
        self.manager = EstadisticasManager(db.session)

    def quejas_por_categoria(self):
        return self.manager.total_quejas_por_categoria()

    def quejas_por_comercio(self):
        return self.manager.total_quejas_por_comercio()

    def quejas_por_departamento(self):
        return self.manager.total_quejas_por_departamento()
