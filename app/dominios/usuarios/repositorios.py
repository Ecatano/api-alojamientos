from app import db
from app.dominios.usuarios.modelos import Usuario


class UsuarioRepositorio:
    """Acceso a la base de datos para el dominio de usuarios."""

    @staticmethod
    def guardar(usuario):
        """Inserta o actualiza un usuario y confirma la transacción."""
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def buscar_por_correo(correo):
        consulta = db.select(Usuario).where(Usuario.correo == correo)
        return db.session.execute(consulta).scalar_one_or_none()

    @staticmethod
    def buscar_por_id(usuario_id):
        return db.session.get(Usuario, usuario_id)

    @staticmethod
    def listar_todos():
        consulta = db.select(Usuario).order_by(Usuario.id)
        return list(db.session.execute(consulta).scalars())