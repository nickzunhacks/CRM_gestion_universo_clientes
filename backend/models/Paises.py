from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

class Paises(SQLModel):
    nombre_pais : str = Field(...)
    nombre_subdivisiones : str = Field(...)

class PaisesId(Paises, table=True):
    __table_args__ = (
        UniqueConstraint('nombre_pais', name='nombre_pais'),
    )
    activo: bool = Field(default=True)
    id_pais: int | None = Field(default=None, primary_key=True)
