from sqlmodel import Field, SQLModel

class Ciudades(SQLModel):
    nombre_ciudad: str = Field(...)
    subdivision: int = Field(foreign_key='subdivisionesid.id_subdivision')

class CiudadesId(Ciudades, table=True):
    id_ciudad: int | None = Field(default=None, primary_key=True)