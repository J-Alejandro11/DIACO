from sqlalchemy import Column, Integer, String, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Comercio(Base):
    __tablename__ = 'Comercios'
    id_comercio = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)

class Departamento(Base):
    __tablename__ = 'Departamentos'
    id_departamento = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)

class Municipio(Base):
    __tablename__ = 'Municipios'
    id_municipio = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    id_departamento = Column(Integer, ForeignKey('Departamentos.id_departamento'))

class Ubicacion(Base):
    __tablename__ = 'Ubicaciones'
    id_ubicacion = Column(Integer, primary_key=True)
    id_comercio = Column(Integer, ForeignKey('Comercios.id_comercio'))
    id_departamento = Column(Integer, ForeignKey('Departamentos.id_departamento'))
    id_municipio = Column(Integer, ForeignKey('Municipios.id_municipio'))

class Queja(Base):
    __tablename__ = 'Quejas'
    id_queja = Column(Integer, primary_key=True)
    id_comercio = Column(Integer, ForeignKey('Comercios.id_comercio'))
    id_ubicacion = Column(Integer, ForeignKey('Ubicaciones.id_ubicacion'))

class ListaComerciosManager:
    def __init__(self, session):
        self.session = session

    def obtener_lista_comercios(self):
        resultados = (
            self.session.query(
                Comercio.nombre.label('comercio'),
                Departamento.nombre.label('departamento'),
                Municipio.nombre.label('municipio'),
                func.count(Queja.id_queja).label('total_quejas')
            )
            .join(Ubicacion, Comercio.id_comercio == Ubicacion.id_comercio)
            .join(Departamento, Ubicacion.id_departamento == Departamento.id_departamento)
            .join(Municipio, Ubicacion.id_municipio == Municipio.id_municipio)
            .join(Queja, (Queja.id_comercio == Comercio.id_comercio) & (Queja.id_ubicacion == Ubicacion.id_ubicacion))
            .group_by(Comercio.nombre, Departamento.nombre, Municipio.nombre)
            .order_by(func.count(Queja.id_queja).desc())
            .all()
        )
        return [
            {
                'comercio': r.comercio,
                'departamento': r.departamento,
                'municipio': r.municipio,
                'total_quejas': r.total_quejas
            }
            for r in resultados
        ]
