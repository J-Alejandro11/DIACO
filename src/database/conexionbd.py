from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    try:
        usuario = "Alejandro"
        password = "Alejandro_tf11"
        servidor = "ALEJANDRO\\SQLEXPRESS"
        base_datos = "DIACO"
        driver = "ODBC+Driver+17+for+SQL+Server"

        # Configura la URI de conexión
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"mssql+pyodbc://{usuario}:{password}@{servidor}/{base_datos}?driver={driver}"
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Inicializa la base de datos con la aplicación Flask
        db.init_app(app)
        print("✅ Base de datos inicializada correctamente")
    except Exception as ex:
        print("❌ Error al inicializar la base de datos:", ex)

# Bloque para ejecutar el archivo directamente
if __name__ == '__main__':
    app = Flask(__name__)  # Crea una instancia de Flask
    init_db(app)           # Llama a la función para inicializar la base de datos