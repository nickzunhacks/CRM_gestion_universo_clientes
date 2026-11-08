class ErroresNegocio(Exception):
    status_code = 400

class NoExiste(ErroresNegocio):
    status_code = 404
    def __init__(self, valor):
        super().__init__(f"{valor} no existe")

class DatosRepetidos(ErroresNegocio):
    status_code = 409
    def __init__(self, valores: list):
        super().__init__(f"los valores {valores} ya se encuentran registrados")

class NoExiteForanea(ErroresNegocio):
    status_code = 422
    def __init__(self, valor: str, foranea: str):
        super().__init__(f"la clave foranea {foranea} no tiene registro con el valor {valor}")

class NoExisteColumna(ErroresNegocio):
    status_code = 400
    def __init__(self, columna: list):
        super().__init__(f"La columna {columna} no existe")

class RegistrosNoBorrados(ErroresNegocio):
    status_code = 409
    def __init__(self, registro: int):
        super().__init__(f"El registro {registro} no se encuentra borrado")