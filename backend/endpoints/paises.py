from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

from backend.models.Paises import Paises
from backend.db.db_config import Conversation
from backend.ErrorHander import DatosRepetidos
from backend.db.operaciones_paises import crear_pais, mostrar_paises, mostrar_paises_borrados, mostrar_un_pais, borrar_pais, restaurar_pais

router = APIRouter()

#-------------------------------------------------------------| GET |-------------------------------------------------------------

@router.get("/paises")
async def get_paises(session: Conversation):
    return await mostrar_paises(session)

@router.get("/pais")
async def get_un_pais(id: int, session: Conversation):
    return await mostrar_un_pais(id, session)



@router.get("/paises-borrados")
async def get_paises_borrados(session: Conversation):
    return await mostrar_paises_borrados(session)

#-------------------------------------------------------------| POST |-------------------------------------------------------------

@router.post("/paises")
async def post_paises(pais: Paises, session: Conversation):
    try:
        return await crear_pais(pais, session)
    except IntegrityError:
        raise DatosRepetidos([pais.nombre_pais])

#-------------------------------------------------------------| UPDATE |-------------------------------------------------------------

@router.post("/paises-borrar")
async def post_paises(id: int, session: Conversation):
    return await borrar_pais(id,session)

@router.post("/pais-recuperar")
async def post_recuperar_pais(id: int, session: Conversation):
    return await restaurar_pais(id,session)

#-------------------------------------------------------------| DELETE |-------------------------------------------------------------
