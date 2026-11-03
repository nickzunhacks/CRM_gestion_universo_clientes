import sqlmodel
from sqlmodel import SQLModel, Field

class TipoIdentificacion(SQLModel):
    nombre_tipo_identificacion: str = Field(...)

class TipoIdentificacionId(TipoIdentificacion, Table=True):
    id_tipo_identificacion: int | None = Field(default=None, primary_key=True)
