from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased
from datetime import datetime

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

class Categoria(Base):
    __tablename__ = 'Categorias'
    id_categoria = Column(Integer, primary_key=True)
    nombre_categoria = Column(String(100), nullable=False)

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
    id_categoria = Column(Integer, ForeignKey('Categorias.id_categoria'))
    descripcion = Column(String, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

class ReporteQuejasManager:
    def __init__(self, session):
        self.session = session

    def obtener_reporte_quejas(self):
        subq = (
            self.session.query(
                Queja.id_comercio,
                Queja.id_ubicacion,
                func.count(Queja.id_queja).label('total_quejas')
            )
            .group_by(Queja.id_comercio, Queja.id_ubicacion)
            .subquery()
        )

        resultados = (
            self.session.query(
                Comercio.nombre.label('comercio'),
                Departamento.nombre.label('departamento'),
                Municipio.nombre.label('municipio'),
                Categoria.nombre_categoria.label('categoria'),
                Queja.descripcion.label('descripcion_queja'),
                Queja.fecha_registro.label('fecha_registro'),
                subq.c.total_quejas.label('total_quejas_por_ubicacion')
            )
            .join(Ubicacion, Queja.id_ubicacion == Ubicacion.id_ubicacion)
            .join(Comercio, Queja.id_comercio == Comercio.id_comercio)
            .join(Departamento, Ubicacion.id_departamento == Departamento.id_departamento)
            .join(Municipio, Ubicacion.id_municipio == Municipio.id_municipio)
            .join(Categoria, Queja.id_categoria == Categoria.id_categoria)
            .join(subq, (Queja.id_comercio == subq.c.id_comercio) & (Queja.id_ubicacion == subq.c.id_ubicacion))
            .order_by(Comercio.nombre, Departamento.nombre, Municipio.nombre, Queja.fecha_registro.desc())
            .all()
        )
        return [
            {
                'comercio': r.comercio,
                'departamento': r.departamento,
                'municipio': r.municipio,
                'categoria': r.categoria,
                'descripcion_queja': r.descripcion_queja,
                'fecha_registro': r.fecha_registro,
                'total_quejas_por_ubicacion': r.total_quejas_por_ubicacion
            }
            for r in resultados
        ]
