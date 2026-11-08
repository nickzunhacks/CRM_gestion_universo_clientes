from fastapi import APIRouter
from backend.models.Ciudades import Ciudades
from backend.db.db_config import Conversation
from backend.db.operaciones_ciudades import crear_ciudad, mostrar_ciudades, mostrar_ciudad, ciudades_borradas, borrar_ciudad, restaurar_ciudad
from backend.helpers.validaciones_repetitivas import validacion_404

router = APIRouter()

#-------------------------------------------------------------| GET |-------------------------------------------------------------


@router.get("/ciudades")
async def get_ciudades(session: Conversation):
    return await mostrar_ciudades(session)

@router.get("/ciudad")
async def get_ciudad(id: int, session: Conversation):
    return await validacion_404(await mostrar_ciudad(id, session), "No se encontro esta ciudad")

@router.get("/ciudades-borradas")
async def get_ciudades_borradas(session: Conversation):
    return await ciudades_borradas(session)

#-------------------------------------------------------------| POST |-------------------------------------------------------------

@router.post("/ciudades")
async def post_ciudades(ciudad: Ciudades, session: Conversation):
    return await crear_ciudad(ciudad, session)

#-------------------------------------------------------------| UPDATE |-------------------------------------------------------------

@router.post("/ciudades-borrar")
async def ciudad_borrar(id: int, session: Conversation):
    return validacion_404(await borrar_ciudad(id, session), "No se encontro esta ciudad para borrar")

@router.post("/ciudad-restaurar")
async def ciudad_restaurar(id: int, session: Conversation):
    return validacion_404(await restaurar_ciudad(id, session), "No se encontro esta ciudad para restaurar")