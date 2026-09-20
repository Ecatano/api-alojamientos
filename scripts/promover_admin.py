import sys

from app import create_app
from app.dominios.usuarios.servicios import UsuarioServicio
from app.errores import ErrorAPI


def main(argumentos):
    """Promueve a administrador al usuario cuyo correo se recibe."""
    if len(argumentos) != 2:
        print("Uso: python -m scripts.promover_admin correo@ejemplo.com")
        return 1

    correo = argumentos[1].strip()
    app = create_app()

    with app.app_context():
        try:
            usuario = UsuarioServicio.promover_admin(correo)
        except ErrorAPI as error:
            print(f"Error: {error.mensaje}")
            return 1

        print(f"Usuario {usuario.correo} promovido al rol: {usuario.rol}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))