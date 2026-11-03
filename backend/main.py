from fastapi import FastAPI
from database.db_config import create_all_tables

app = FastAPI(lifespan=create_all_tables)

@app.get("/")
async def root():
    return {"message": "Hello World"}