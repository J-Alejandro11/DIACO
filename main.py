from flask import Flask
from src.routes import bp
from src.database.conexionbd import init_db, db


app = Flask(
    __name__,
    template_folder="src/templates",
    static_folder="src/static"
)

# Inicializa la base de datos
init_db(app)

# Registrar el Blueprint
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)