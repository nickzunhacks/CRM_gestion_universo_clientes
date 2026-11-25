from fastapi import APIRouter
from backend.models import IndustriaId, Industria
from backend.db.operaciones_industria import crear_industria, mostrar_industrias, mostrar_una_industria,mostrar_industrias_borradas, borrar_industria, restautrar_industria
from backend.db.db_config import Conversation

router = APIRouter()

#-------------------------------------------------------------| GET |-------------------------------------------------------------

@router.get("/industrias")
async def get_industrias(session: Conversation):
    return await mostrar_industrias(session)

@router.get("/industria")
async def get_una_industria(id: int, session: Conversation):
    return await mostrar_una_industria(id, session)

@router.get("/industrias-borradas")
async def get_industrias_borradas(session: Conversation):
    return await mostrar_industrias_borradas(session)

#-------------------------------------------------------------| POST |-------------------------------------------------------------

@router.post("/industrias")
async def post_industrias(industria: Industria, session: Conversation):
    return await crear_industria(industria, session)

#-------------------------------------------------------------| UPDATE |-------------------------------------------------------------

@router.post("/industria-borrar")
async def industria_borrar(id: int, session: Conversation):
    return await borrar_industria(id, session)

@router.post("/industria-restaurar")
async def industria_restaurar(id: int, session: Conversation):
    return await restautrar_industria(id, session)