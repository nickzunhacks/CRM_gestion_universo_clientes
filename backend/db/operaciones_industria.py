from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from backend.ErrorHander import DatosRepetidos
from backend.models.Industria import Industria, IndustriaId
from backend.db.operaciones_genericas import crear, mostrar_todos, buscar_uno, borrar_uno, mostrar_borrados, restaurar_registro

# operaciones POST
async def crear_industria(industria: Industria, session: Session) -> IndustriaId:
    try:
        return await crear(IndustriaId, industria, session)
    except IntegrityError:
        raise DatosRepetidos([industria.nombre_industria])

# operaciones GET
async def mostrar_industrias(session: Session) -> IndustriaId | None:
    return await mostrar_todos(IndustriaId, session)

async def mostrar_una_industria(id: int, session: Session) -> IndustriaId | None:
    return await buscar_uno(IndustriaId, id, session)

async def mostrar_industrias_borradas(session: Session) -> IndustriaId | None:
    return await mostrar_borrados(IndustriaId, session)

# operaciones UPDATE

async def borrar_industria(id: int, session: Session) -> IndustriaId | None:
    return await borrar_uno(IndustriaId, id, session)

async def restautrar_industria(id: int, session: Session) -> IndustriaId | None:
    return await restaurar_registro(IndustriaId, id, session)