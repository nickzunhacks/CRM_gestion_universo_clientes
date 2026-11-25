from sqlalchemy.exc import IntegrityError
from backend.db.operaciones_genericas import crear_con_foreign, mostrar_todos, buscar_uno, borrar_uno, mostrar_borrados, restaurar_registro, mostrar_por_filtro_foraneo
from backend.models.Subdivisiones import Subdivisiones, SubdivisionesId
from backend.models.Paises import PaisesId
from backend.ErrorHander import DatosRepetidos
from sqlmodel import Session

# operaciones post

async def crear_subdivision(subdivision: Subdivisiones, session: Session) -> SubdivisionesId:
    try:
        return await crear_con_foreign(SubdivisionesId, {"id_pais":PaisesId}, subdivision, session)
    except IntegrityError:
        raise DatosRepetidos([subdivision.nombre_subdivision, subdivision.id_pais])

# operaciones get

async def mostrar_subdivisiones(session: Session) -> SubdivisionesId:
    return await mostrar_todos(SubdivisionesId, session)

async def mostrar_una_subdivision(id: int, session: Session) -> SubdivisionesId:
    return await buscar_uno(SubdivisionesId, id,  session)

async def mostrar_subdivisiones_borradas(session: Session) -> SubdivisionesId:
    return await mostrar_borrados(SubdivisionesId, session)

async def mostrar_subdivisiones_pais(id_pais: int, session: Session) -> SubdivisionesId:
    return await mostrar_por_filtro_foraneo(SubdivisionesId, {id_pais:["id_pais", PaisesId]}, session)

# operaciones update

async def borrar_subdivision(id: int, session: Session) -> SubdivisionesId:
    return await borrar_uno(SubdivisionesId, id, session)

async def restaurar_subdivision(id: int, session: Session) -> SubdivisionesId:
    return await restaurar_registro(SubdivisionesId, id, session)