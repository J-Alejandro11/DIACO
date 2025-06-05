from flask import Blueprint, render_template, request, jsonify
from src.controllers.queja_controller import DepartamentoController
from src.database.conexionbd import db
import os
from src.controllers.estadisticas_controller import EstadisticasController

bp = Blueprint('main', __name__)

# Inicializar el controlador
queja_controller = DepartamentoController()
estadisticas_controller = EstadisticasController()

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

@bp.route('/api/quejas', methods=['POST'])
def api_insertar_queja():
    data = request.get_json()
    nombre_comercio = data.get('nombre_comercio')
    nombre_departamento = data.get('nombre_departamento')
    nombre_municipio = data.get('nombre_municipio')
    nombre_categoria = data.get('nombre_categoria')
    descripcion_queja = data.get('descripcion_queja')
    try:
        resultado = queja_controller.insertar_queja_completa(
            nombre_comercio,
            nombre_departamento,
            nombre_municipio,
            nombre_categoria,
            descripcion_queja
        )
        return jsonify({'success': True, **resultado}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@bp.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

@bp.route('/api/estadisticas/categorias')
def api_estadisticas_categorias():
    return jsonify(estadisticas_controller.quejas_por_categoria())

@bp.route('/api/estadisticas/comercios')
def api_estadisticas_comercios():
    return jsonify(estadisticas_controller.quejas_por_comercio())

@bp.route('/api/estadisticas/departamentos')
def api_estadisticas_departamentos():
    return jsonify(estadisticas_controller.quejas_por_departamento())