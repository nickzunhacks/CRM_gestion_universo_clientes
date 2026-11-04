from sqlmodel import Session
from backend.models.Empresa import Empresa, EmpresaId
from backend.db.operaciones_genericas import crear, mostrar_todos, buscar_uno, borrar_uno, mostrar_borrados, restaurar_registro

async def crear_empresa(empresa: Empresa, session: Session) -> EmpresaId | None:
    return await crear(EmpresaId, empresa, session)

async def mostrar_una_empresa(id: int, session: Session) -> EmpresaId | None:
    return await buscar_uno(EmpresaId, id, session)

async def mostrar_empresas(session: Session) -> EmpresaId | None:
    return await mostrar_todos(EmpresaId, session)

async def mostrar_empresas_borradas(session: Session) -> EmpresaId | None:
    return await mostrar_borrados(EmpresaId, session)

async def borrar_empresa(id: int, session: Session) -> EmpresaId | None:
    return await borrar_uno(EmpresaId, id, session)

async def restaurar_empresa(id: int, session: Session) -> EmpresaId | None:
    return await restaurar_registro(EmpresaId, id, session)