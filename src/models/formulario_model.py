from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()

class Departamento(Base):
    __tablename__ = 'Departamentos'
    id_departamento = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    municipios = relationship("Municipio", back_populates="departamento")

class Municipio(Base):
    __tablename__ = 'Municipios'
    id_municipio = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    id_departamento = Column(Integer, ForeignKey('Departamentos.id_departamento'))
    departamento = relationship("Departamento", back_populates="municipios")

class Categoria(Base):
    __tablename__ = 'Categorias'
    id_categoria = Column(Integer, primary_key=True)
    nombre_categoria = Column(String(100), nullable=False)

class Comercio(Base):
    __tablename__ = 'Comercios'
    id_comercio = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)

class DepartamentoManager:
    def __init__(self, session):
        self.session = session

    def obtener_nombres(self):
        resultados = self.session.query(Departamento.nombre).all()
        return [r[0] for r in resultados]

    def obtener_municipios_por_departamento(self, nombre_departamento):
        """
        Devuelve una lista con los nombres de los municipios de un departamento dado su nombre.
        Equivalente a la consulta SQL proporcionada.
        """
        resultados = (
            self.session.query(Municipio.nombre)
            .join(Departamento, Municipio.id_departamento == Departamento.id_departamento)
            .filter(Departamento.nombre == nombre_departamento)
            .order_by(Municipio.nombre)
            .all()
        )
        return [r[0] for r in resultados]

    def obtener_categorias(self):
        resultados = self.session.query(Categoria.nombre_categoria).all()
        return [r[0] for r in resultados]

    def insertar_comercio(self, nombre):
        """
        Inserta un nuevo comercio en la base de datos.
        Equivalente a: INSERT INTO Comercios (nombre) VALUES (...)
        """
        try:
            nuevo_comercio = Comercio(nombre=nombre)
            self.session.add(nuevo_comercio)
            self.session.commit()
            return nuevo_comercio
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Error al insertar comercio: {str(e)}") 