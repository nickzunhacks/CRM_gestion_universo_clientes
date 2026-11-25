from sqlmodel import Session, select
from backend.ErrorHander import RegistroBorrado, NoExiteForanea, NoExisteColumna, RegistrosNoBorrados, NoExiste

#-------------------------------------------------------------| POST |-------------------------------------------------------------

async def crear(tabla, datos, session: Session):
    nuevo = tabla.model_validate(datos)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

async def crear_con_foreign(tabla_guardar, validaciones: dict, datos, session: Session): #dic es un clave_foranea: tabla, para saber si el valor de foranea si esta en la tabla pricipal

    for foreign, tabla in validaciones.items():
        valor = getattr(datos, foreign)
        if await buscar_uno(tabla, valor, session) is None:
            raise NoExiteForanea(valor=valor, foranea=foreign)

    nuevo = tabla_guardar.model_validate(datos)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo

#-------------------------------------------------------------| GET |-------------------------------------------------------------

async def buscar_uno(tabla, id: int, session: Session):
    x = session.get(tabla, id)
    if x and not x.activo:                          #.activo debe estar en todas las tablas, ya que se maneja borrado logico en todas las tablas
        raise RegistroBorrado(id)
    return x

async def mostrar_todos(tabla, session: Session):
    return session.exec(select(tabla).where(tabla.activo==True)).all()

async def mostrar_por_filtro_foraneo(tabla_buscar, filtro: dict, session: Session): # dic es: valor : [columna foranea, tabla (el modelo)]

    # verificar que la categoria de la clave foranea si existe y no esta borrada

    consulta = select(tabla_buscar).where(tabla_buscar.activo == True)

    for valor, foranea in filtro.items():
        if await buscar_uno(foranea[1], valor, session) is None:
            raise NoExiste(valor=valor)
        consulta = consulta.where(getattr(tabla_buscar, foranea[0]) == valor)

    return session.exec(consulta).all()

async def mostrar_borrados(tabla, session: Session):
    return session.exec(select(tabla).where(tabla.activo==False)).all()

#-------------------------------------------------------------| UPDATE |-------------------------------------------------------------

async def borrar_uno(tabla, id: int, session: Session):
    x = await buscar_uno(tabla, id, session)
    if x:
        if not x.activo:
            raise RegistroBorrado(id)
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
            return x
        else:
            raise RegistrosNoBorrados(registro=id)
    raise NoExiste(id)