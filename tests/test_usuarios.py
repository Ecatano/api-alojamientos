RUTA_REGISTRO = "/api/v1/usuarios/registro"
RUTA_LOGIN = "/api/v1/usuarios/login"
RUTA_PERFIL = "/api/v1/usuarios/perfil"

DATOS_VALIDOS = {
    "correo": "ana@ejemplo.com",
    "contrasena": "123456",
}


def test_registro_exitoso_responde_201(client):
    respuesta = client.post(RUTA_REGISTRO, json=DATOS_VALIDOS)

    assert respuesta.status_code == 201


def test_registro_con_correo_invalido_responde_400(client):
    datos = {**DATOS_VALIDOS, "correo": "correo-sin-arroba"}

    respuesta = client.post(RUTA_REGISTRO, json=datos)

    assert respuesta.status_code == 400


def test_registro_con_correo_duplicado_responde_409(client):
    client.post(RUTA_REGISTRO, json=DATOS_VALIDOS)

    respuesta = client.post(RUTA_REGISTRO, json=DATOS_VALIDOS)

    assert respuesta.status_code == 409


def test_login_valido_responde_200_con_token(client):
    client.post(RUTA_REGISTRO, json=DATOS_VALIDOS)

    respuesta = client.post(RUTA_LOGIN, json=DATOS_VALIDOS)

    assert respuesta.status_code == 200
    assert "access_token" in respuesta.get_json()


def test_login_invalido_responde_401(client):
    client.post(RUTA_REGISTRO, json=DATOS_VALIDOS)
    datos = {**DATOS_VALIDOS, "contrasena": "contrasena-incorrecta"}

    respuesta = client.post(RUTA_LOGIN, json=datos)

    assert respuesta.status_code == 401


def test_perfil_sin_token_responde_401(client):
    respuesta = client.get(RUTA_PERFIL)

    assert respuesta.status_code == 401


def test_perfil_con_token_valido_responde_200(client, token_usuario):
    respuesta = client.get(
        RUTA_PERFIL,
        headers={"Authorization": f"Bearer {token_usuario}"},
    )

    assert respuesta.status_code == 200