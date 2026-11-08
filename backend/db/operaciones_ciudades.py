from backend.db.operaciones_genericas import crear, mostrar_todos, mostrar_borrados, buscar_uno, borrar_uno, restaurar_registro
from backend.models.Ciudades import Ciudades, CiudadesId
from sqlmodel import Session

# operaciones POST

async def crear_ciudad(ciudad: Ciudades, session: Session) -> CiudadesId:
    return await crear(CiudadesId, ciudad, session)

# operaciones GET

async def mostrar_ciudades(session: Session) -> CiudadesId:
    return await mostrar_todos(CiudadesId, session)

async def mostrar_ciudad(id: int, session: Session) -> CiudadesId:
    return await buscar_uno(CiudadesId, id, session)

async def ciudades_borradas(session: Session) -> CiudadesId:
    return await mostrar_borrados(CiudadesId, session)

# operaciones UPDATE

async def borrar_ciudad(id: int, session: Session) -> CiudadesId:
    return await borrar_uno(CiudadesId, id, session)

async def restaurar_ciudad(id: int, session: Session) -> CiudadesId:
    return await restaurar_registro(CiudadesId, id, session)