from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from app.dominios.usuarios.modelos import PerfilUsuario, Usuario
from app.dominios.usuarios.repositorios import UsuarioRepositorio
from app.errores import ErrorAPI


class UsuarioServicio:
    """Reglas de negocio del dominio de usuarios."""

    @staticmethod
    def registrar(datos):
        """Registra un usuario nuevo con su perfil vacío.

        Lanza ErrorAPI 409 si el correo ya está registrado.
        """
        if UsuarioRepositorio.buscar_por_correo(datos["correo"]):
            raise ErrorAPI("El correo ya se encuentra registrado.", 409)

        usuario = Usuario(
            correo=datos["correo"],
            contrasena=generate_password_hash(datos["contrasena"]),
            rol="usuario",
        )
        usuario.perfil = PerfilUsuario()

        return UsuarioRepositorio.guardar(usuario)

    @staticmethod
    def iniciar_sesion(datos):
        """Valida las credenciales y devuelve un token JWT.

        Lanza ErrorAPI 401 si el correo o la contraseña no coinciden.
        """
        usuario = UsuarioRepositorio.buscar_por_correo(datos["correo"])

        if usuario is None or not check_password_hash(
            usuario.contrasena, datos["contrasena"]
        ):
            raise ErrorAPI("Credenciales inválidas.", 401)

        return {
            "access_token": UsuarioServicio._generar_token(usuario),
            "usuario": usuario.to_dict(),
        }

    @staticmethod
    def obtener_perfil(usuario_id):
        """Devuelve los datos del usuario autenticado y su perfil.

        Lanza ErrorAPI 404 si el usuario ya no existe.
        """
        usuario = UsuarioRepositorio.buscar_por_id(usuario_id)

        if usuario is None:
            raise ErrorAPI("Usuario no encontrado.", 404)

        return {
            "usuario": usuario.to_dict(),
            "perfil": usuario.perfil.to_dict() if usuario.perfil else None,
        }

    @staticmethod
    def listar_usuarios():
        """Devuelve todos los usuarios registrados (uso administrativo)."""
        return [
            usuario.to_dict() for usuario in UsuarioRepositorio.listar_todos()
        ]

    @staticmethod
    def promover_admin(correo):
        """Cambia el rol de un usuario a admin.

        Lanza ErrorAPI 404 si el correo no está registrado.
        """
        usuario = UsuarioRepositorio.buscar_por_correo(correo)

        if usuario is None:
            raise ErrorAPI("Usuario no encontrado.", 404)

        usuario.rol = "admin"
        return UsuarioRepositorio.guardar(usuario)

    @staticmethod
    def _generar_token(usuario):
        """Genera un JWT firmado con HS256 que vence según JWT_EXP_MINUTES."""
        ahora = datetime.now(timezone.utc)
        vencimiento = ahora + timedelta(
            minutes=current_app.config["JWT_EXP_MINUTES"]
        )
        payload = {
            "sub": str(usuario.id),
            "iat": ahora,
            "exp": vencimiento,
        }
        return jwt.encode(
            payload,
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )