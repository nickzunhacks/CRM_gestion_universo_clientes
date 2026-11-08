from sqlmodel import Field, SQLModel

class CodigoCiiu(SQLModel):
    codigo_ciiu: str = Field(...)
    descripcion: str = Field(...)
    pais_codigo_ciiu: int = Field(foreign_key="paisesid.id_pais")

class CodigoCiiuId(CodigoCiiu, table=True):
    activo: bool = Field(default=True)
    id_codigo_ciiu: int | None = Field(default=None, primary_key=True)
