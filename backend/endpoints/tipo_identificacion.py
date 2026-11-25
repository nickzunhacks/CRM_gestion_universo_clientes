from fastapi import APIRouter
from backend.db.operaciones_tipoid import mostrar_tipos_id, mostrar_tipo_id, mostrar_tipos_id_borrads, crear_tipo_identificacion, borrar_tipo_id, restaurar_tipo_id
from backend.db.db_config import Conversation
from backend.models import TipoIdentificacion, TipoIdentificacionId

router = APIRouter()

#-------------------------------------------------------------| GET |-------------------------------------------------------------

@router.get("/tipos-id")
async def get_tipos_id(session: Conversation):
    return await mostrar_tipos_id(session)

@router.get("/tipo-id")
async def get_tipo_id(id: int, session: Conversation):
    return await mostrar_tipo_id(id, session)

@router.get("/tipo-id-borrados")
async def get_tipo_id_borrados(session: Conversation):
    return await mostrar_tipos_id_borrads(session)

#-------------------------------------------------------------| POST |-------------------------------------------------------------

@router.post("/tipos-id")
async def post_tipo_id(tipo: TipoIdentificacion, session: Conversation):
    return await crear_tipo_identificacion(tipo, session)

#-------------------------------------------------------------| UPDATE |-------------------------------------------------------------

@router.post("/tipo-id-borrar")
async def tipo_id_borrar(id: int, session: Conversation):
    return await borrar_tipo_id(id, session)

@router.post("/tipo-id-restaurar")
async def tipo_id_restaurar(id: int, session: Conversation):
    return await restaurar_tipo_id(id, session)