from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from backend.helpers.validaciones_repetitivas import validacion_404
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
    return validacion_404(await mostrar_una_empresa(id, session), "Empresa no encontrada")

@router.get("/empresas-borradas")
async def get_empresas_borradas(session: Conversation):
    return await mostrar_empresas_borradas(session)

#-------------------------------------------------------------| POST |-------------------------------------------------------------

@router.post("/empresa")
async def post_empresa(empresa: Empresa, session: Conversation):
    try:
        empresa = await crear_empresa(empresa, session)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="No se puede registrar una empresa con el mismo pais, numero y tipo de identificacion")
    return empresa

#-------------------------------------------------------------| UPDATE |-------------------------------------------------------------

@router.post("/empresa-borrar")
async def delete_empresa(id: int, session: Conversation):
    return validacion_404(await borrar_empresa(id, session), "No se encontro una empresa para borrar")

@router.post("/empresa-recuperar")
async def recuperar_empresa(id: int, session: Conversation):
    return validacion_404(await restaurar_empresa(id, session), "No se encontro una empresa para recuperar")