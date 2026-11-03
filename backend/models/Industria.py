from sqlmodel import Field, SQLModel

class Industria(SQLModel):
    nombre_industria: str = Field(...)

class IndustriaId(Industria, Table=True):
    id_industria: int = Field(primary_key=True)