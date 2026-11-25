from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from backend.models.Empresa import Empresa
from backend.db.db_config import Conversation
from backend.db.operaciones_empresa import crear_empresa, mostrar_empresas, borrar_empresa, mostrar_empresas_borradas, mostrar_una_empresa, restaurar_empresa

router = APIRouter()

#-------------------------------------------------------------| GET |-------------------------------------------------------------

@router.get("/empresas")
async def get_empresas(session: Conversation):
    return await mostrar_empresas(session)

@router.get("/empresa")
async def get_empresa_una(id: int, session: Conversation):
    return await mostrar_una_empresa(id, session)

@router.get("/empresas-borradas")
async def get_empresas_borradas(session: Conversation):
    return await mostrar_empresas_borradas(session)

#-------------------------------------------------------------| POST |-------------------------------------------------------------

@router.post("/empresa")
async def post_empresa(empresa: Empresa, session: Conversation):
    return await crear_empresa(empresa, session)

#-------------------------------------------------------------| UPDATE |-------------------------------------------------------------

@router.post("/empresa-borrar")
async def delete_empresa(id: int, session: Conversation):
    return await borrar_empresa(id, session)

@router.post("/empresa-recuperar")
async def recuperar_empresa(id: int, session: Conversation):
    return await restaurar_empresa(id, session)