from sqlalchemy.exc import IntegrityError
from backend.ErrorHander import DatosRepetidos
from backend.models.TipoIdentificacion import TipoIdentificacion, TipoIdentificacionId
from backend.db.operaciones_genericas import crear, buscar_uno, mostrar_todos, mostrar_borrados, borrar_uno, restaurar_registro
from sqlmodel import Session

# operaciones POST
async def crear_tipo_identificacion(tipo: TipoIdentificacion, session: Session) -> TipoIdentificacionId:
    try:
        return await crear(TipoIdentificacionId, tipo, session)
    except IntegrityError:
        raise DatosRepetidos([tipo.nombre_tipo_identificacion])

# Operaciones GET
async def mostrar_tipos_id(session: Session) -> list[TipoIdentificacionId]:
    return await mostrar_todos(TipoIdentificacionId, session)

async def mostrar_tipo_id(id: int, session: Session) -> TipoIdentificacionId | None:
    return await buscar_uno(TipoIdentificacionId, id, session)

async def mostrar_tipos_id_borrads(session: Session) -> list[TipoIdentificacionId]:
    return await mostrar_borrados(TipoIdentificacionId, session)

# Operaciones UPTDATE
async def borrar_tipo_id(int: id, session: Session) -> TipoIdentificacionId:
    return await borrar_uno(TipoIdentificacionId, int, session)

async def restaurar_tipo_id(int: id, session: Session) -> TipoIdentificacionId:
    return await restaurar_registro(TipoIdentificacionId, int, session)