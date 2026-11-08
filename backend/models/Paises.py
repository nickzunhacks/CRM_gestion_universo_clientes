from sqlmodel import SQLModel, Field

class Paises(SQLModel):
    nombre_pais : str = Field(...)
    nombre_subdivisiones : str = Field(...)

class PaisesId(Paises, table=True):
    activo: bool = Field(default=True)
    id_pais: int | None = Field(default=None, primary_key=True)
