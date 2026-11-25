from backend.endpoints import empresas, paises, ciudades, subdivisiones, industria, tipo_identificacion
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.ErrorHander import ErroresNegocio
from backend.db.db_config import create_all_tables

app = FastAPI(lifespan=create_all_tables)

@app.exception_handler(ErroresNegocio)
async def exception_handler(request: Request, exc: ErroresNegocio):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc)}
    )

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(empresas.router)
app.include_router(paises.router)
app.include_router(ciudades.router)
app.include_router(subdivisiones.router)
app.include_router(industria.router)
app.include_router(tipo_identificacion.router)