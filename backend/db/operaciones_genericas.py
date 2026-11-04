from sqlmodel import SQLModel, Session, select

async def crear(tabla, datos, session: Session):
    nuevo = tabla.model_validate(datos)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

async def buscar_uno(tabla, id: int, session: Session):
    x = session.get(tabla, id)
    if x and not x.activo:
        return None
    return x

async def mostrar_todos(tabla, session: Session):
    return session.exec(select(tabla).where(tabla.activo==True)).all()

async def mostrar_borrados(tabla, session: Session):
    return session.exec(select(tabla).where(tabla.activo==False)).all()

async def borrar_uno(tabla, id: int, session: Session):
    x = await buscar_uno(tabla, id, session)
    if x:
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