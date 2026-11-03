from sqlmodel import Field, SQLModel

class EstadosLegales(SQLModel):
    estado_legal: str = Field(...)

class EstadosLegalesId(SQLModel, Table=True):
    id_estado_legal: int | None = Field(default=None, primary_key=True)