class ErrorNegocio(Exception):
    """Error esperado que se informa al usuario con el código HTTP indicado."""

    def __init__(self, status_code: int, mensaje: str):
        super().__init__(mensaje)
        self.status_code = status_code
        self.mensaje = mensaje
