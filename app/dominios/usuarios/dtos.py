from marshmallow import EXCLUDE, Schema, fields, validate


class RegistroUsuarioDTO(Schema):
    """Valida los datos de entrada para registrar un usuario."""

    class Meta:
        unknown = EXCLUDE

    correo = fields.Email(
        required=True,
        validate=validate.Length(max=120),
        error_messages={
            "required": "El correo es obligatorio.",
            "invalid": "El correo no tiene un formato válido.",
        },
    )
    contrasena = fields.String(
        required=True,
        validate=validate.Length(min=6, max=128),
        error_messages={"required": "La contraseña es obligatoria."},
    )


class LoginUsuarioDTO(Schema):
    """Valida los datos de entrada para iniciar sesión."""

    class Meta:
        unknown = EXCLUDE

    correo = fields.Email(
        required=True,
        error_messages={
            "required": "El correo es obligatorio.",
            "invalid": "El correo no tiene un formato válido.",
        },
    )
    contrasena = fields.String(
        required=True,
        error_messages={"required": "La contraseña es obligatoria."},
    )