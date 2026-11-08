from fastapi import HTTPException

def validacion_404(resultado, mensaje: str):
    if not resultado:
        raise HTTPException(status_code=404, detail=mensaje)
    return resultado

def validacion_422(resultado):
    if not resultado:
        raise HTTPException(status_code=422, detail="Alguno de los datos enviados no esta registrado")
    return resultado