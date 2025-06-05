from flask import Blueprint, render_template, request, jsonify, make_response
from src.controllers.queja_controller import DepartamentoController
from src.database.conexionbd import db
import os
from src.controllers.estadisticas_controller import EstadisticasController
from src.controllers.usuario_controller import UsuarioController
from src.controllers.quejas_total_controller import QuejasTotalController
from sqlalchemy import func, distinct
from src.controllers.revision_quejas_controller import QuejasDetalladasController
from src.controllers.lista_comercios_controller import ComerciosUbicacionesController
from src.controllers.reporte_quejas_controller import ReporteQuejasController
from fpdf import FPDF

bp = Blueprint('main', __name__)

# Inicializar el controlador
queja_controller = DepartamentoController()
estadisticas_controller = EstadisticasController()
usuario_controller = UsuarioController()
quejas_total_controller = QuejasTotalController()
revision_quejas_controller = QuejasDetalladasController()
lista_comercios_controller = ComerciosUbicacionesController()
reporte_quejas_controller = ReporteQuejasController()

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

@bp.route('/loginAdministrador')
def loginAdministrador():
    return render_template('administrador/login.html')

@bp.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')
    print('Usuario recibido:', usuario)
    print('Contraseña recibida:', contrasena)
    user = usuario_controller.autenticar(usuario, contrasena)
    if user:
        return jsonify({'success': True, 'id_usuario': user.id_usuario, 'usuario': user.usuario})
    else:
        return jsonify({'success': False, 'error': 'Usuario o contraseña incorrectos'}), 401

@bp.route('/panel-admin')
def panel_admin():
    return render_template('administrador/panel-admin.html')

@bp.route('/api/estadisticas/total-quejas')
def api_total_quejas():
    total = quejas_total_controller.total_quejas()
    return jsonify({'total_quejas': total})

@bp.route('/api/estadisticas/total-comercios')
def api_total_comercios():
    total = quejas_total_controller.total_comercios_reportados()
    return jsonify({'total_comercios_reportados': total})

@bp.route('/api/quejas/detalladas')
def api_quejas_detalladas():
    data = revision_quejas_controller.obtener_quejas_detalladas()
    return jsonify(data)

@bp.route('/api/comercios/lista')
def api_lista_comercios():
    data = lista_comercios_controller.obtener_lista_comercios()
    return jsonify(data)

@bp.route('/api/reportes/quejas/pdf')
def api_reporte_quejas_pdf():
    data = reporte_quejas_controller.obtener_reporte_quejas()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, "Reporte de Quejas", ln=True, align='C')
    pdf.ln(5)
    # Encabezados
    headers = ["Comercio", "Departamento", "Municipio", "Categoria", "Descripcion", "Fecha", "Total Quejas Ubicación"]
    for header in headers:
        pdf.cell(30, 8, header, border=1)
    pdf.ln()
    # Filas
    for row in data:
        pdf.cell(30, 8, str(row['comercio'])[:15], border=1)
        pdf.cell(30, 8, str(row['departamento'])[:15], border=1)
        pdf.cell(30, 8, str(row['municipio'])[:15], border=1)
        pdf.cell(30, 8, str(row['categoria'])[:15], border=1)
        pdf.cell(30, 8, str(row['descripcion_queja'])[:15], border=1)
        fecha = row['fecha_registro']
        if fecha:
            fecha = fecha.strftime('%Y-%m-%d %H:%M')
        else:
            fecha = ''
        pdf.cell(30, 8, fecha, border=1)
        pdf.cell(30, 8, str(row['total_quejas_por_ubicacion']), border=1)
        pdf.ln()
    response = make_response(pdf.output(dest='S').encode('latin1'))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=reporte_quejas.pdf'
    return response

@bp.route('/api/reportes/quejas')
def api_reporte_quejas():
    data = reporte_quejas_controller.obtener_reporte_quejas()
    return jsonify(data)