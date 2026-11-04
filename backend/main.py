from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError

from backend.models import Empresa
from backend.db.db_config import create_all_tables, Conversation
from backend.db.operaciones_empresa import crear_empresa, mostrar_empresas, borrar_empresa, mostrar_empresas_borradas, mostrar_una_empresa, restaurar_empresa

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/empresas")
async def get_empresas(session: Conversation):
    return await mostrar_empresas(session)

@app.get("/empresa-una")
async def get_empresa_una(id: int, session: Conversation):
    return await mostrar_una_empresa(id, session)

@app.get("/empresas-borradas")
async def get_empresas_borradas(session: Conversation):
    return await mostrar_empresas_borradas(session)

@app.post("/empresa")
async def post_empresa(empresa: Empresa, session: Conversation):
    try:
        empresa = await crear_empresa(empresa, session)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="No se puede registrar una empresa con el mismo pais, numero y tipo de identificacion")
    return await crear_empresa(empresa, session)

@app.post("/empresa-borrar")
async def delete_empresa(id: int, session: Conversation):
    empresa = await borrar_empresa(id, session)
    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    return empresa

@app.post("/empresa-recuperar")
async def recuperar_empresa(id: int, session: Conversation):
    empresa = await restaurar_empresa(id, session)
    if not empresa:
        raise HTTPException(status_code=404, detail="No se encontro empresa para recuperar")
    return empresa