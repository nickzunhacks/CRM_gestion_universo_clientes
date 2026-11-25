from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint

class Subdivisiones(SQLModel):
    nombre_subdivision: str = Field(...)
    id_pais: int = Field(foreign_key='paisesid.id_pais')

class SubdivisionesId(Subdivisiones, table=True):
    __table_args__ = (
        UniqueConstraint("nombre_subdivision", "id_pais", name="uniq_nombre_subdivision_pais"),
    )
    activo: bool = Field(default=True)
    id_subdivision: int | None = Field(default=None, primary_key=True)