from backend.endpoints import empresas, paises, ciudades, subdivisiones
from fastapi import FastAPI
from backend.db.db_config import create_all_tables, Conversation

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(empresas.router)
app.include_router(paises.router)
app.include_router(ciudades.router)
app.include_router(subdivisiones.router)