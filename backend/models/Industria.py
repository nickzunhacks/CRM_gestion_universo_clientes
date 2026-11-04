from sqlmodel import Field, SQLModel

class Industria(SQLModel):
    nombre_industria: str = Field(...)

class IndustriaId(Industria, table=True):
    id_industria: int | None = Field(default=None, primary_key=True)