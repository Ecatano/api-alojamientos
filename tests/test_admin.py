RUTA_ADMIN_USUARIOS = "/api/v1/admin/usuarios"


def test_admin_usuarios_con_usuario_normal_responde_403(client, token_usuario):
    respuesta = client.get(
        RUTA_ADMIN_USUARIOS,
        headers={"Authorization": f"Bearer {token_usuario}"},
    )

    assert respuesta.status_code == 403


def test_admin_usuarios_con_administrador_responde_200(client, token_admin):
    respuesta = client.get(
        RUTA_ADMIN_USUARIOS,
        headers={"Authorization": f"Bearer {token_admin}"},
    )

    assert respuesta.status_code == 200