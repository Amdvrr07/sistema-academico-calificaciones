from pydantic import BaseModel
from datetime import date

class EstudianteCrear(BaseModel):
    nombre: str
    cedula: str


class EstudianteRespuesta(BaseModel):
    id: int
    nombre: str
    cedula: str

    class Config:
        from_attributes = True