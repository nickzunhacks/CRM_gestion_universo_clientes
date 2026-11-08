from sqlmodel import Session
from backend.models.Paises import Paises, PaisesId
from backend.db.operaciones_genericas import crear, mostrar_todos, buscar_uno, borrar_uno, mostrar_borrados, restaurar_registro

# operaciones post

async def crear_pais(pais: Paises, session: Session) -> PaisesId | None:
    return await crear(PaisesId, pais, session)

# operaciones get

async def mostrar_un_pais(id: int, session: Session) -> PaisesId | None:
    return await buscar_uno(PaisesId, id, session)

async def mostrar_paises(session: Session) -> PaisesId | None:
    return await mostrar_todos(PaisesId, session)

async def mostrar_paises_borrados(session: Session) -> PaisesId | None:
    return await mostrar_borrados(PaisesId, session)

# operaciones update

async def borrar_pais(id: int, session: Session) -> PaisesId | None:
    return await borrar_uno(PaisesId, id, session)

async def restaurar_pais(id: int, session: Session) -> PaisesId | None:
    return await restaurar_registro(PaisesId, id, session)