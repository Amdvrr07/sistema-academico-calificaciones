from pydantic import BaseModel


class ReporteEstudiantes(BaseModel):
    total_estudiantes: int


class ReportePromedio(BaseModel):
    estudiante_id: int
    promedio: float


class ReporteAprobado(BaseModel):
    estudiante_id: int
    promedio: float


class ReporteGeneral(BaseModel):
    total_estudiantes: int
    total_aprobados: int
    total_reprobados: int