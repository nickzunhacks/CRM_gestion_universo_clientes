from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint

class CodigoCiiu(SQLModel):
    codigo_ciiu: str = Field(...)
    descripcion: str = Field(...)
    id_pais: int = Field(foreign_key="paisesid.id_pais")
    id_industria: int = Field(foreign_key="industriaid.id_industria")

class CodigoCiiuId(CodigoCiiu, table=True):
    __table__args__ = (
        UniqueConstraint("codigo_ciiu", "id_industria", "id_pais", name="unique_id_codigo_ciiu_id_industria"),
    )
    activo: bool = Field(default=True)
    id_codigo_ciiu: int | None = Field(default=None, primary_key=True)
