from fastapi import APIRouter
from backend.controllers import secretaria

router = APIRouter(
    prefix="/secretaria",
    tags=["Secretaría y Horarios"]
)


# Horarios

@router.get("/horarios")
async def obtener_horarios():
    return await secretaria.obtener_horarios()

@router.get("/horarios/{horario_id}")
async def obtener_horario(horario_id: int):
    return await secretaria.obtener_horario(horario_id)

@router.post("/horarios")
async def crear_horario(horario_data: dict):
    return await secretaria.crear_horario(horario_data)

@router.put("/horarios/{horario_id}")
async def actualizar_horario(
    horario_id: int,
    horario_data: dict
):
    return await secretaria.actualizar_horario(
        horario_id,
        horario_data
    )

@router.delete("/horarios/{horario_id}")
async def eliminar_horario(horario_id: int):
    return await secretaria.eliminar_horario(horario_id)

# Aulas

@router.get("/aulas")
async def obtener_aulas():
    return await secretaria.obtener_aulas()

# Docentes

@router.get("/docentes")


async def obtener_docentes():
<<<<<<< HEAD
    return await secretaria.obtener_docentes()
=======
    return await secretaria.obtener_docentes()


>>>>>>> 71797ebcf8838159b2cf3553b6e750c3896ae10a
