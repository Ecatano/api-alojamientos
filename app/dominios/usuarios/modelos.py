from app import db


class Usuario(db.Model):
    """Cuenta de acceso a la API."""

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="usuario")

    perfil = db.relationship(
        "PerfilUsuario",
        back_populates="usuario",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        """Datos públicos del usuario. Nunca incluye la contraseña."""
        return {
            "id": self.id,
            "correo": self.correo,
            "rol": self.rol,
        }


class PerfilUsuario(db.Model):
    """Datos personales asociados a un usuario (relación 1:1)."""

    __tablename__ = "perfiles"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    apellido = db.Column(db.String(80))
    telefono = db.Column(db.String(20))
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        unique=True,
        nullable=False,
    )

    usuario = db.relationship("Usuario", back_populates="perfil")

    def to_dict(self):
        return {
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
        }