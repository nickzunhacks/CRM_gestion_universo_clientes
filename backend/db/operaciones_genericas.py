from sqlmodel import Session, select
from sqlalchemy import inspect

#-------------------------------------------------------------| POST |-------------------------------------------------------------

async def crear(tabla, datos, session: Session):
    nuevo = tabla.model_validate(datos)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

async def crear_con_foreign(tabla_guardar, validaciones: dict, datos, session: Session):

    for foreign, tabla in validaciones.items():
        valor = getattr(datos, foreign)
        if await buscar_uno(tabla, valor, session) is None:
            return None

    nuevo = tabla_guardar.model_validate(datos)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

#-------------------------------------------------------------| GET |-------------------------------------------------------------

async def buscar_uno(tabla, id: int, session: Session):
    x = session.get(tabla, id)
    if x and not x.activo:
        raise ValueError("Registro borrado")
    return x

async def mostrar_todos(tabla, session: Session):
    return session.exec(select(tabla).where(tabla.activo==True)).all()

async def mostrar_por_filtro(tabla, filtro: dict, session: Session): # dic es un columna:valor el cual es el filtro
    consulta = select(tabla).where(tabla.actico == True)
    for columna, valor in filtro.items():
        consulta = consulta.where(getattr(tabla, columna) == valor)

async def mostrar_borrados(tabla, session: Session):
    return session.exec(select(tabla).where(tabla.activo==False)).all()

#-------------------------------------------------------------| UPDATE |-------------------------------------------------------------

async def borrar_uno(tabla, id: int, session: Session):
    x = await buscar_uno(tabla, id, session)
    if x:
        if not x.activo:
            raise ValueError("Registro ya esta borrado")
        x.activo = False
        session.add(x)
        session.commit()
        session.refresh(x)
    return x

async def restaurar_registro(tabla, id: int, session: Session):
    x = session.get(tabla, id)
    if x:
        if not x.activo:
            x.activo = True
            session.add(x)
            session.commit()
            session.refresh(x)
        else:
            return None
    return x