from sqlalchemy import func
from src.models.formulario_model import Categoria, Comercio, Departamento, Queja, Ubicacion

class EstadisticasManager:
    def __init__(self, session):
        self.session = session

    def total_quejas_por_categoria(self):
        resultados = (
            self.session.query(Categoria.nombre_categoria.label('categoria'), func.count(Queja.id_queja).label('total'))
            .join(Queja, Queja.id_categoria == Categoria.id_categoria)
            .group_by(Categoria.nombre_categoria)
            .order_by(func.count(Queja.id_queja).desc())
            .all()
        )
        return [{'categoria': r.categoria, 'total': r.total} for r in resultados]

    def total_quejas_por_comercio(self):
        resultados = (
            self.session.query(Comercio.nombre.label('comercio'), func.count(Queja.id_queja).label('total_quejas'))
            .join(Queja, Queja.id_comercio == Comercio.id_comercio)
            .group_by(Comercio.nombre)
            .order_by(func.count(Queja.id_queja).desc())
            .all()
        )
        return [{'comercio': r.comercio, 'total_quejas': r.total_quejas} for r in resultados]

    def total_quejas_por_departamento(self):
        resultados = (
            self.session.query(Departamento.nombre.label('departamento'), func.count(Queja.id_queja).label('total'))
            .join(Ubicacion, Ubicacion.id_departamento == Departamento.id_departamento)
            .join(Queja, Queja.id_ubicacion == Ubicacion.id_ubicacion)
            .group_by(Departamento.nombre)
            .order_by(func.count(Queja.id_queja).desc())
            .all()
        )
        return [{'departamento': r.departamento, 'total': r.total} for r in resultados]
