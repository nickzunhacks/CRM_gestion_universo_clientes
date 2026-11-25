from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

class TipoIdentificacion(SQLModel):
    nombre_tipo_identificacion: str = Field(...)

class TipoIdentificacionId(TipoIdentificacion, table=True):
    __table_args__ = (
        UniqueConstraint('nombre_tipo_identificacion', name='unique_tipo_identificacion_id'),
    )
    activo: bool = Field(default=True)
    id_tipo_identificacion: int | None = Field(default=None, primary_key=True)
