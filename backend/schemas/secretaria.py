from pydantic import BaseModel
from datetime import date


class EstudianteCrear(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    correo: str


class EstudianteRespuesta(BaseModel):
    id: int
    nombre: str
    apellido: str
    cedula: str
    correo: str

    class Config:
        from_attributes = True


class MatriculaCrear(BaseModel):
    estudiante_id: int
    curso_id: int


class MatriculaRespuesta(BaseModel):
    id: int
    estudiante_id: int
    curso_id: int
    fecha_matricula: date

    class Config:
        from_attributes = True


class HorarioRespuesta(BaseModel):
    id: int
    curso: str
    dia: str
    hora_inicio: str
    hora_fin: str

    class Config:
        from_attributes = True