from src.models.formulario_model import DepartamentoManager
from src.database.conexionbd import db

class DepartamentoController:
    def __init__(self):
        self.manager = DepartamentoManager(db.session)

    def obtener_nombres_departamentos(self):
        """
        Devuelve una lista de nombres de departamentos.
        """
        return self.manager.obtener_nombres()

    def obtener_municipios_por_departamento(self, nombre_departamento):
        """
        Devuelve una lista de nombres de municipios para un departamento dado su nombre.
        """
        return self.manager.obtener_municipios_por_departamento(nombre_departamento)

    def obtener_categorias(self):
        """
        Devuelve una lista de nombres de categorías.
        """
        return self.manager.obtener_categorias()

    def insertar_comercio(self, nombre):
        """
        Inserta un nuevo comercio en la base de datos.
        """
        return self.manager.insertar_comercio(nombre) 
