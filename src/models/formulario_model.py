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

    def insertar_queja_completa(self, nombre_comercio, nombre_departamento, nombre_municipio, nombre_categoria, descripcion_queja):
        """
        Inserta una queja completa y retorna los IDs de los campos relacionados.
        """
        try:
            # 1. Buscar departamento
            departamento = self.session.query(Departamento).filter_by(nombre=nombre_departamento).first()
            if not departamento:
                raise Exception("El departamento no existe.")
            
            # 2. Buscar municipio
            municipio = self.session.query(Municipio).filter_by(
                nombre=nombre_municipio,
                id_departamento=departamento.id_departamento
            ).first()
            if not municipio:
                raise Exception("El municipio no existe para el departamento especificado.")
            
            # 3. Buscar o insertar comercio
            comercio = self.session.query(Comercio).filter_by(nombre=nombre_comercio).first()
            if not comercio:
                comercio = Comercio(nombre=nombre_comercio)
                self.session.add(comercio)
                self.session.commit()
            
            # 4. Buscar o insertar ubicación
            ubicacion = self.session.query(Ubicacion).filter_by(
                id_comercio=comercio.id_comercio,
                id_departamento=departamento.id_departamento,
                id_municipio=municipio.id_municipio
            ).first()
            if not ubicacion:
                ubicacion = Ubicacion(
                    id_comercio=comercio.id_comercio,
                    id_departamento=departamento.id_departamento,
                    id_municipio=municipio.id_municipio
                )
                self.session.add(ubicacion)
                self.session.commit()
            
            # 5. Buscar categoría
            categoria = self.session.query(Categoria).filter_by(nombre_categoria=nombre_categoria).first()
            if not categoria:
                raise Exception("La categoría especificada no existe.")
            
            # 6. Insertar la queja
            queja = Queja(
                id_comercio=comercio.id_comercio,
                id_ubicacion=ubicacion.id_ubicacion,
                id_categoria=categoria.id_categoria,
                descripcion=descripcion_queja
            )
            self.session.add(queja)
            self.session.commit()
            
            # Retornar los IDs
            return {
                'id_queja': queja.id_queja,
                'id_comercio': comercio.id_comercio,
                'id_ubicacion': ubicacion.id_ubicacion,
                'id_categoria': categoria.id_categoria
            }
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Error al insertar la queja: {str(e)}") 