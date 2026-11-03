from sqlmodel import Field, SQLModel

class Subdivisiones(SQLModel):
    nombre_subdivision: str = Field(...)
    pais: int = Field(foreign_key='paisesid.id_pais')

class SubdivisionesId(Subdivisiones, table=True):
    id_subdivision: int | None = Field(default=None, primary_key=True)