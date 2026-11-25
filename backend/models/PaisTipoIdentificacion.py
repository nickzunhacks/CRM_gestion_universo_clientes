from sqlmodel import SQLModel, Field

class PaisTipoIdentificacion(SQLModel):
    id_pais: int = Field(foreign_key='paisesid.id_pais')
    id_tipo_identificacion: int = Field(foreign_key="tipoidentificacionid.id_tipo_identificacion")
    PRIMARY_KEY = ("id_pais", "id_tipo_identificacion")