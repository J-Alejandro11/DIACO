from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
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

class QuejasDetalladasManager:
    def __init__(self, session):
        self.session = session

    def obtener_quejas_detalladas(self):
        """
        Devuelve una lista de diccionarios con la información detallada de cada queja,
        equivalente a la consulta SQL proporcionada.
        """
        resultados = (
            self.session.query(
                Queja.id_queja.label('id_queja'),
                Comercio.nombre.label('nombre_comercio'),
                Departamento.nombre.label('departamento'),
                Municipio.nombre.label('municipio'),
                Categoria.nombre_categoria.label('categoria_queja'),
                Queja.descripcion.label('descripcion'),
                Queja.fecha_registro.label('fecha_registro')
            )
            .join(Comercio, Queja.id_comercio == Comercio.id_comercio)
            .join(Ubicacion, Queja.id_ubicacion == Ubicacion.id_ubicacion)
            .join(Departamento, Ubicacion.id_departamento == Departamento.id_departamento)
            .join(Municipio, Ubicacion.id_municipio == Municipio.id_municipio)
            .join(Categoria, Queja.id_categoria == Categoria.id_categoria)
            .order_by(Queja.fecha_registro.desc())
            .all()
        )
        return [
            {
                'id_queja': r.id_queja,
                'nombre_comercio': r.nombre_comercio,
                'departamento': r.departamento,
                'municipio': r.municipio,
                'categoria_queja': r.categoria_queja,
                'descripcion': r.descripcion,
                'fecha_registro': r.fecha_registro
            }
            for r in resultados
        ]