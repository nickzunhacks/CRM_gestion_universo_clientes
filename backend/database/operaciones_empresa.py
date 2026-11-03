from sqlmodel import Session
from backend.models.Empresa import Empresa, EmpresaId

async def crear_empresa(empresa: Empresa, session: Session) -> EmpresaId:
    nueva_empresa = EmpresaId.model_validate(empresa)
    session.add(nueva_empresa)
    session.commit()
    session.refresh(nueva_empresa)
    return nueva_empresa