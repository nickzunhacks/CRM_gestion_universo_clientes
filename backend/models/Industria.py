from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint

class Industria(SQLModel):
    nombre_industria: str = Field(...)

class IndustriaId(Industria, table=True):
    __table_args__ = (
        UniqueConstraint(
            'nombre_industria',
            name='nombre_industria'
        ),
    )
    activo: bool = Field(default=True)
    id_industria: int | None = Field(default=None, primary_key=True)