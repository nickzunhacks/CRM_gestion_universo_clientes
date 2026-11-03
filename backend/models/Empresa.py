from sqlmodel import SQLModel, Field
from datetime import date


class Empresa(SQLModel):
    fecha_registro: date = date.today()
    pais_empresa: int = Field(foreign_key='paisesid.id_pais') # estandarizacion de paises
    tipo_identificacion_empresa: int = Field(foreign_key='tipoidentificacionid.id_tipo_identificacion') # estandarizacion de tipo id de empresa
    numero_identificacion_empresa: int = Field(...)
    razon_social: str = Field(...)
    fecha_inicio_operaciones: date | None = Field(default=None)
    numero_matricula: int | None = Field(default=None)
    estado_legal_empresa: int | None = Field(default=None, foreign_key='estadoslegalesid.id_estado_legal') # estandarizacion de estados legales
    codigo_ciiu: int | None = Field(default=None, foreign_key='codigociiuid.id_codigo_ciiu') # estandarizacion de codigos ciiu con su descripcion
    industria: int | None = Field(default=None, foreign_key='industriaid.id_industria') # estandarizacion de tipos de industrias
    url_pagina_web: str | None  = Field(default=None)
    direccion_oficina_principal: str | None  = Field(default=None)
    subdivision: int | None = Field(default=None, foreign_key='subdivisionesid.id_subdivision') # estandarizacion de subdivisiones que pertenecen a cada pais
    ciudad: int | None = Field(default=None, foreign_key='ciudadesid.id_ciudad') # estandarizacion de ciudades que pertenecen a cada subidvision
    url_linkedin: str | None = Field(default=None)
    activo: bool = Field(default=True) # El registro no se borra, solo se desactiva
    observaciones: str | None = Field(default=None)

class EmpresaId(SQLModel):
    id_empresa: int | None = Field(default=None, primary_key=True)
