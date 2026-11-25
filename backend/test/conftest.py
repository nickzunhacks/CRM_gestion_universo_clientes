import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel
from sqlmodel.pool import StaticPool
from backend.main import app
from backend.db.db_config import get_session

@pytest.fixture()
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False}, # Permite conexiones con mas de un hilo
        poolclass=StaticPool, # Evita crear una db nueva por cada conexion
    )

    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture()
def client(session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session # Antes de empezar test, se remplaza la funcion original get_session, por la que creamos en este archivo, para crear una db temporal y eliminar las tablas en cada test, esto porque en los endpoints llamamos a get_session, pero en este caso al hacer que get_session se remplace por session de este archivo, los endpoints usaran esta funcion en vez de la orginal
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear() # el remplazo de la funcion por otra se llama inyeccionde de dependencias, app guarda un diccionario que siempre mira al recibir una peticion. aqui limpiamos el diccionario que se crea al hacer el proceso de hacer que si se encuentra get_session: ejecute session pero de este archivo. Para que esto no pase en produccion se limpia en cada prueba, o si no este diccionario se mantiene y al llamar un endpoint en produccion se llamaria esta funcion en vez de la original