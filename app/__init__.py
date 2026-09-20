from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from app.config import Config
from app.errores import ErrorAPI

API_VERSION = "v1"

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_overrides=None):
    """Crea y configura la aplicación Flask.

    config_overrides: diccionario opcional cuyos valores reemplazan la
    configuración por defecto. Se utiliza en las pruebas automatizadas.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=app.config["CORS_ALLOWED_ORIGINS"])

    # Se importa aquí para evitar importaciones circulares: los modelos
    # necesitan el objeto db definido arriba en este mismo módulo.
    from app.dominios.usuarios.controladores import admin_bp, usuarios_bp

    app.register_blueprint(usuarios_bp, url_prefix="/api/v1/usuarios")
    app.register_blueprint(admin_bp, url_prefix="/api/v1/admin")

    @app.errorhandler(ValidationError)
    def manejar_error_validacion(error):
        return (
            jsonify({"error": "Datos inválidos.", "detalles": error.messages}),
            400,
        )

    @app.errorhandler(ErrorAPI)
    def manejar_error_api(error):
        return jsonify({"error": error.mensaje}), error.codigo

    @app.get("/health")
    def health():
        return {
            "status": "ok",
            "service": "alojamientos-api",
            "version": API_VERSION,
        }, 200

    return app