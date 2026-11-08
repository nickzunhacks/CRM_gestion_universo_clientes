from backend.db.operaciones_genericas import crear_con_foreign, mostrar_todos, buscar_uno, borrar_uno, mostrar_borrados, restaurar_registro, mostrar_por_filtro
from backend.models.Subdivisiones import Subdivisiones, SubdivisionesId
from backend.models.Paises import PaisesId
from sqlmodel import Session

# operaciones post

async def crear_subdivision(subdivision: Subdivisiones, session: Session) -> SubdivisionesId:
    return await crear_con_foreign(SubdivisionesId, {"pais":PaisesId}, subdivision, session)

# operaciones get

async def mostrar_subdivisiones(session: Session) -> SubdivisionesId:
    return await mostrar_todos(SubdivisionesId, session)

async def mostrar_una_subdivision(id: int, session: Session) -> SubdivisionesId:
    return await buscar_uno(SubdivisionesId, id,  session)

async def mostrar_subdivisiones_borradas(session: Session) -> SubdivisionesId:
    return await mostrar_borrados(SubdivisionesId, session)

async def mostrar_subdivisiones_pais(id_pais: int, session: Session) -> SubdivisionesId:
    return await mostrar_por_filtro(SubdivisionesId, {"pais":id_pais}, session)

# operaciones update

async def borrar_subdivision(id: int, session: Session) -> SubdivisionesId:
    return await borrar_uno(SubdivisionesId, id, session)

async def restaurar_subdivision(id: int, session: Session) -> SubdivisionesId:
    return await restaurar_registro(SubdivisionesId, id, session)