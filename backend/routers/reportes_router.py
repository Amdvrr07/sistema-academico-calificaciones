from fastapi import APIRouter
from backend.controllers import reportes

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

# Reporte de horarios

@router.get("/horarios")
async def reporte_horarios():
    return await reportes.reporte_horarios()

# Reporte de aulas

@router.get("/aulas")
async def reporte_aulas():
    return await reportes.reporte_aulas()

# Reporte de docentes

@router.get("/docentes")
async def reporte_docentes():
    return await reportes.reporte_docentes()

# Reporte académico

@router.get("/academico")
async def reporte_academico():
    return await reportes.reporte_academico()

# Estadísticas generales

@router.get("/estadisticas")
async def estadisticas():
    return await reportes.estadisticas()

