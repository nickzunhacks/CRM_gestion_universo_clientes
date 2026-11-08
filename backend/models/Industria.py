from sqlmodel import Field, SQLModel

class Industria(SQLModel):
    nombre_industria: str = Field(...)
    codigo_ciiu: int = Field(foreign_key="codigociiuid.id_codigo_ciiu")

class IndustriaId(Industria, table=True):
    activo: bool = Field(default=True)
    id_industria: int | None = Field(default=None, primary_key=True)