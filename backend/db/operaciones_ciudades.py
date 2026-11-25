from sqlalchemy.exc import IntegrityError

from backend.ErrorHander import DatosRepetidos
from backend.ErrorHander import NoExiste
from backend.db.operaciones_genericas import crear_con_foreign, mostrar_todos, mostrar_borrados, buscar_uno, borrar_uno, restaurar_registro, mostrar_por_filtro_foraneo
from backend.models.Ciudades import Ciudades, CiudadesId
from backend.models.Subdivisiones import SubdivisionesId
from backend.models.Paises import PaisesId
from sqlmodel import Session, select, join

# operaciones POST

async def crear_ciudad(ciudad: Ciudades, session: Session) -> CiudadesId:
    try:
        return await crear_con_foreign(CiudadesId, {"id_subdivision":SubdivisionesId}, ciudad, session)
    except IntegrityError:
        raise DatosRepetidos([ciudad.nombre_ciudad])

# operaciones GET

async def mostrar_ciudades(session: Session) -> list[CiudadesId]:
    return await mostrar_todos(CiudadesId, session)

async def mostrar_ciudad(id: int, session: Session) -> CiudadesId:
    return await buscar_uno(CiudadesId, id, session)

async def mostrar_ciudades_por_subdivision(id: int, session: Session) -> CiudadesId:
    return await mostrar_por_filtro_foraneo(CiudadesId, {id:["id_subdivision", SubdivisionesId]}, session)

async def mostrar_ciudades_por_pais(id: int, session: Session) -> list[CiudadesId]:
    if not await buscar_uno(PaisesId, id, session):
        raise NoExiste(id)
    consulta = (select(CiudadesId)
                .join(SubdivisionesId, SubdivisionesId.id_subdivision == CiudadesId.id_subdivision)
                .where(SubdivisionesId.id_pais == id,
                       CiudadesId.activo == True,
                       SubdivisionesId.activo == True
                       )
                )
    return session.exec(consulta).all()

async def ciudades_borradas(session: Session) -> list[CiudadesId]:
    return await mostrar_borrados(CiudadesId, session)

# operaciones UPDATE

async def borrar_ciudad(id: int, session: Session) -> CiudadesId:
    return await borrar_uno(CiudadesId, id, session)

async def restaurar_ciudad(id: int, session: Session) -> CiudadesId:
    return await restaurar_registro(CiudadesId, id, session)