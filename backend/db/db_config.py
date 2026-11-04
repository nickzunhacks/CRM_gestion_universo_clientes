from sqlmodel import Session, create_engine, SQLModel
from fastapi import Depends, FastAPI
from typing import Annotated
from dotenv import load_dotenv
import os

load_dotenv()
URL = os.getenv("sqlite") # base de datos de pruebas

engine = create_engine(URL) # crear el motor con segun la DB que depende de la URL

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine) # crea tablas segun los modelos que tenga table=True

    print("------------------------------------------------| TABLAS |------------------------------------------------")
    for tabla in SQLModel.metadata.sorted_tables:
        print(f"\nTabla: {tabla.name}")
        for columna in tabla.columns:
            print(f"  - {columna.name}: {columna.type} "
                  f"(PK={columna.primary_key}, FK={columna.foreign_keys}, nullable={columna.nullable})")
    yield

def get_session() -> Session:
    with Session(engine) as session:
        yield session # retorna la session

Conversation = Annotated[Session, Depends(get_session)] # nos ayuda a evitar pone Depends(get_session) en cada endpoint


