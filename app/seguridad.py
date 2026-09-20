from functools import wraps

import jwt
from flask import current_app, request

from app.dominios.usuarios.repositorios import UsuarioRepositorio
from app.errores import ErrorAPI


def _obtener_usuario_id():
    """Lee el Bearer Token de la petición y devuelve el id del usuario.

    Lanza ErrorAPI 401 si el token falta, es inválido o está vencido.
    """
    encabezado = request.headers.get("Authorization", "")
    partes = encabezado.split()

    if len(partes) != 2 or partes[0].lower() != "bearer":
        raise ErrorAPI("Se requiere autorización.", 401)

    try:
        payload = jwt.decode(
            partes[1],
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"],
            options={"require": ["sub", "iat", "exp"]},
        )
        return int(payload["sub"])
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise ErrorAPI("Token inválido o expirado.", 401)


def requiere_token(funcion):
    """Protege un endpoint: exige un JWT válido y entrega usuario_id."""

    @wraps(funcion)
    def envoltura(*args, **kwargs):
        usuario_id = _obtener_usuario_id()
        return funcion(usuario_id, *args, **kwargs)

    return envoltura


def requiere_admin(funcion):
    """Protege un endpoint: exige un JWT válido y rol admin.

    El rol se consulta en la base de datos en cada petición, no se toma
    del token, para que un cambio de rol tenga efecto inmediato.
    """

    @wraps(funcion)
    def envoltura(*args, **kwargs):
        usuario_id = _obtener_usuario_id()
        usuario = UsuarioRepositorio.buscar_por_id(usuario_id)

        if usuario is None:
            raise ErrorAPI("Token inválido o expirado.", 401)

        if usuario.rol != "admin":
            raise ErrorAPI("Se requiere rol de administrador.", 403)

        return funcion(usuario_id, *args, **kwargs)

    return envoltura