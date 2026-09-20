from flask import Blueprint, jsonify, request

from app.dominios.usuarios.dtos import LoginUsuarioDTO, RegistroUsuarioDTO
from app.dominios.usuarios.servicios import UsuarioServicio
from app.seguridad import requiere_admin, requiere_token

usuarios_bp = Blueprint("usuarios", __name__)
admin_bp = Blueprint("admin", __name__)


@usuarios_bp.post("/registro")
def registro():
    """Registra un usuario nuevo."""
    datos = RegistroUsuarioDTO().load(request.get_json(silent=True) or {})
    usuario = UsuarioServicio.registrar(datos)

    return (
        jsonify(
            {
                "mensaje": "Usuario registrado correctamente.",
                "usuario": usuario.to_dict(),
            }
        ),
        201,
    )


@usuarios_bp.post("/login")
def login():
    """Inicia sesión y devuelve un token de acceso."""
    datos = LoginUsuarioDTO().load(request.get_json(silent=True) or {})
    resultado = UsuarioServicio.iniciar_sesion(datos)

    return jsonify(resultado), 200


@usuarios_bp.get("/perfil")
@requiere_token
def perfil(usuario_id):
    """Devuelve el perfil del usuario autenticado."""
    resultado = UsuarioServicio.obtener_perfil(usuario_id)

    return jsonify(resultado), 200


@admin_bp.get("/usuarios")
@requiere_admin
def listar_usuarios(usuario_id):
    """Lista todos los usuarios. Solo para administradores."""
    return jsonify({"usuarios": UsuarioServicio.listar_usuarios()}), 200