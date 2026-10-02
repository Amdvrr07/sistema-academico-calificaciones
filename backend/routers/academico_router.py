from fastapi import APIRouter
from backend.controllers import academico

router = APIRouter(
    prefix="/academico",
    tags=["Académico y Calificaciones"]
)

# Materias

@router.get("/materias")
async def obtener_materias():
    return await academico.obtener_materias()

# Calificaciones

@router.get("/calificaciones")
async def obtener_calificaciones():
    return await academico.obtener_calificaciones()

@router.get("/calificaciones/{estudiante_id}")
async def obtener_calificaciones_estudiante(
    estudiante_id: int
):
    return await academico.obtener_calificaciones_estudiante(
        estudiante_id
    )

@router.post("/calificaciones")
async def registrar_calificacion(
    calificacion_data: dict
):
    return await academico.registrar_calificacion(
        calificacion_data
    )

@router.put("/calificaciones/{calificacion_id}")
async def actualizar_calificacion(
    calificacion_id: int,
    calificacion_data: dict
):
    return await academico.actualizar_calificacion(
        calificacion_id,
        calificacion_data
    )

# Promedios

@router.get("/promedio/{estudiante_id}")
async def calcular_promedio(
    estudiante_id: int
):
    return await academico.calcular_promedio(
        estudiante_id
    )


