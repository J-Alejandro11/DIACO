from flask import Blueprint, render_template, request, jsonify
from src.controllers.departamento_controller import DepartamentoController
from src.database.conexionbd import db
import os

bp = Blueprint('main', __name__)

# Inicializar el controlador
queja_controller = DepartamentoController()

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/formulario')
def formulario():
    return render_template('formulario.html')

@bp.route('/api/departamentos')
def api_departamentos():
    nombres = queja_controller.obtener_nombres_departamentos()
    return jsonify(nombres)

@bp.route('/api/municipios')
def api_municipios():
    nombre_departamento = request.args.get('departamento')
    municipios = queja_controller.obtener_municipios_por_departamento(nombre_departamento)
    return jsonify(municipios)

@bp.route('/api/categorias')
def api_categorias():
    categorias = queja_controller.obtener_categorias()
    return jsonify(categorias)

@bp.route('/api/comercios', methods=['POST'])
def api_insertar_comercio():
    data = request.get_json()
    nombre = data.get('nombre')
    try:
        comercio = queja_controller.insertar_comercio(nombre)
        return jsonify({'success': True, 'id_comercio': comercio.id_comercio, 'nombre': comercio.nombre})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400
