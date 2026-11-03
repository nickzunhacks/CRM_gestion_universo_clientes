from sqlmodel import Field, SQLModel

class CodigoCiiu(SQLModel):
    codigo_ciiu: str = Field(...)
    descripcion: str = Field(...)

class CodigoCiiuId(CodigoCiiu, Table=True):
    id_codigo_ciiu: int = Field(primary_key=True)