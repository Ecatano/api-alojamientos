import pytest

from app import create_app, db
from app.dominios.usuarios.repositorios import UsuarioRepositorio


@pytest.fixture
def app():
    """Aplicación de pruebas con una base SQLite en memoria."""
    aplicacion = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "clave-solo-para-pruebas-automatizadas-1234",
            "JWT_EXP_MINUTES": 15,
        }
    )

    with aplicacion.app_context():
        db.create_all()
        yield aplicacion
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def token_usuario(client):
    """Registra un usuario de prueba y devuelve su token JWT."""
    datos = {"correo": "usuario@ejemplo.com", "contrasena": "123456"}
    client.post("/api/v1/usuarios/registro", json=datos)
    respuesta = client.post("/api/v1/usuarios/login", json=datos)

    return respuesta.get_json()["access_token"]


@pytest.fixture
def token_admin(client):
    """Crea un administrador de prueba y devuelve su token JWT."""
    datos = {"correo": "admin@ejemplo.com", "contrasena": "123456"}
    client.post("/api/v1/usuarios/registro", json=datos)

    usuario = UsuarioRepositorio.buscar_por_correo(datos["correo"])
    usuario.rol = "admin"
    UsuarioRepositorio.guardar(usuario)

    respuesta = client.post("/api/v1/usuarios/login", json=datos)

    return respuesta.get_json()["access_token"]