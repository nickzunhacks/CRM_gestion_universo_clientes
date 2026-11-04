from sqlmodel import Field, SQLModel

class CodigoCiiu(SQLModel):
    codigo_ciiu: str = Field(...)
    descripcion: str = Field(...)

class CodigoCiiuId(CodigoCiiu, table=True):
    id_codigo_ciiu: int | None = Field(default=None, primary_key=True)
