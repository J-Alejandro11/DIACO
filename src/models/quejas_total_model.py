from sqlalchemy import Column, Integer, func, distinct, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Solo necesitas el modelo Queja si no lo tienes ya importado
class Queja(Base):
    __tablename__ = 'Quejas'
    id_queja = Column(Integer, primary_key=True)
    id_comercio = Column(Integer, ForeignKey('Comercios.id_comercio'))
    # ... otros campos si los necesitas

class QuejasTotalManager:
    def __init__(self, session):
        self.session = session

    def total_quejas(self):
        """
        Devuelve el total de quejas en la base de datos.
        Equivalente a: SELECT COUNT(*) AS Total_Quejas FROM Quejas;
        """
        total = self.session.query(func.count(Queja.id_queja)).scalar()
        return total

    def total_comercios_reportados(self):
        """
        Devuelve el total de comercios distintos que han sido reportados en la tabla Quejas.
        Equivalente a: SELECT COUNT(DISTINCT id_comercio) AS Comercios_Reportados FROM Quejas;
        """
        total = self.session.query(func.count(distinct(Queja.id_comercio))).scalar()
        return total
