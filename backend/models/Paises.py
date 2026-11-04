from sqlmodel import SQLModel, Field

class Paises(SQLModel):
    nombre_pais : str = Field(...)

class PaisesId(Paises, table=True):
    id_pais: int | None = Field(default=None, primary_key=True)
