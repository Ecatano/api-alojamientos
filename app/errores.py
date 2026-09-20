class ErrorAPI(Exception):
    """Error controlado de la API.

    Lleva un mensaje legible y el código HTTP que debe recibir el cliente.
    """

    def __init__(self, mensaje, codigo=400):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo