from pydantic import BaseModel, Field


class CalificacionCrear(BaseModel):
    estudiante_id: int
    materia_id: int
    calificacion: float = Field(
        ge=0,
        le=100
    )


class CalificacionRespuesta(BaseModel):
    id: int
    estudiante_id: int
    materia_id: int
    calificacion: float

    class Config:
        from_attributes = True


class PromedioRespuesta(BaseModel):
    estudiante_id: int
    promedio: float


class MateriaCrear(BaseModel):
    nombre: str
    descripcion: str


class MateriaRespuesta(BaseModel):
    id: int
    nombre: str
    descripcion: str

    class Config:
        from_attributes = True