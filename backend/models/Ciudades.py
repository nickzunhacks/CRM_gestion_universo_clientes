from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint

class Ciudades(SQLModel):
    nombre_ciudad: str = Field(...)
    id_subdivision: int = Field(foreign_key='subdivisionesid.id_subdivision')

class CiudadesId(Ciudades, table=True):
    __table_args__ = (
        UniqueConstraint('nombre_ciudad', name='uniq_nombre_ciudad'),
    )
    activo: bool = Field(default=True)
    id_ciudad: int | None = Field(default=None, primary_key=True)