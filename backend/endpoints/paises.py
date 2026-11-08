from fastapi import APIRouter
from backend.helpers.validaciones_repetitivas import validacion_404
from backend.models.Paises import Paises
from backend.db.db_config import Conversation
from backend.db.operaciones_paises import crear_pais, mostrar_paises, mostrar_paises_borrados, mostrar_un_pais, borrar_pais, restaurar_pais

router = APIRouter()

#-------------------------------------------------------------| GET |-------------------------------------------------------------

@router.get("/paises")
async def get_paises(session: Conversation):
    return await mostrar_paises(session)

@router.get("/pais")
async def get_un_pais(id: int, session: Conversation):
    return validacion_404(await mostrar_un_pais(id, session), "Pais no encontrado")



@router.get("/paises-borrados")
async def get_paises_borrados(session: Conversation):
    return await mostrar_paises_borrados(session)

#-------------------------------------------------------------| POST |-------------------------------------------------------------

@router.post("/paises")
async def post_paises(pais: Paises, session: Conversation):
    return await crear_pais(pais, session)


#-------------------------------------------------------------| UPDATE |-------------------------------------------------------------

@router.post("/paises-borrar")
async def post_paises(id: int, session: Conversation):
    return validacion_404(await borrar_pais(id,session), "No se encontro una pais para borrar")

@router.post("/pais-recuperar")
async def post_recuperar_pais(id: int, session: Conversation):
    return validacion_404(await restaurar_pais(id,session), "No se encontro un pais para restaurar")

#-------------------------------------------------------------| DELETE |-------------------------------------------------------------
