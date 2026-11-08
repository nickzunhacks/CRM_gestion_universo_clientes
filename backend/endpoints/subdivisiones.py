from fastapi import APIRouter
from backend.helpers.validaciones_repetitivas import validacion_404, validacion_422
from backend.models.Subdivisiones import Subdivisiones
from backend.db.operaciones_subdivisiones import crear_subdivision, mostrar_subdivisiones, mostrar_una_subdivision, mostrar_subdivisiones_borradas, borrar_subdivision, restaurar_subdivision, mostrar_subdivisiones_pais
from backend.db.db_config import Conversation

router = APIRouter()

#-------------------------------------------------------------| GET |-------------------------------------------------------------

@router.get("/subdivisiones")
async def get_subdivisiones(session: Conversation):
    return await mostrar_subdivisiones(session)

@router.get("/subdivision")
async def get_una_subdivision(id: int, session: Conversation):
    return validacion_404(await mostrar_una_subdivision(id, session), "No se encontro esta subdivision")

@router.get("/subdivisiones-borradas")
async def get_subdivisiones_borradas(session: Conversation):
    return await mostrar_subdivisiones_borradas(session)

@router.get("/subdivisiones-pais")
async def get_subdivisiones_pais(pais: int, session: Conversation):
    return await mostrar_subdivisiones_pais(pais, session)

#-------------------------------------------------------------| POST |-------------------------------------------------------------

@router.post("/subdivisiones")
async def post_subdivision(subdivision: Subdivisiones, session: Conversation):
    return validacion_422(await crear_subdivision(subdivision, session))

#-------------------------------------------------------------| UPDATE |-------------------------------------------------------------

@router.post("/subdivision-borrar")
async def subdivision_borrar(id: int, session: Conversation):
    return validacion_404(await borrar_subdivision(id, session), "No se encontro esta subdivision para borrar")

@router.post("/subdivisiones-restaurar")
async def subdivisiones_restaurar(id: int, session: Conversation):
    return validacion_404(await restaurar_subdivision(id, session), "No se encontro esta subdivision para restaurar")