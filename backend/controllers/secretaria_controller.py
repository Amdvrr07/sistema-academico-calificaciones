from fastapi import HTTPException
from fastapi_controllers import Controller, get, post, put, delete
from sqlalchemy.future import select
from backend.database import get_db_session 
from backend.models.secretaria_model import Profesores
from backend.models.base import Bloque, Aula 

class SecretariaController(Controller):
    
    @get("/horarios")
    async def obtener_horarios(self):
        async with get_db_session() as db:
            result = await db.execute(select(Bloque))
            return result.scalars().all()

    @get("/horarios/{horario_id}")
    async def obtener_horario(self, horario_id: int):
        async with get_db_session() as db:
            result = await db.execute(select(Bloque).where(Bloque.bloque_id == horario_id))
            horario = result.scalars().first()
            
            if not horario:
                raise HTTPException(status_code=404, detail="Horario no encontrado")
            return horario

    @post("/horarios")
    async def crear_horario(self, horario_data: dict):
        async with get_db_session() as db:
            nuevo_horario = Bloque(**horario_data)
            db.add(nuevo_horario)
            await db.commit()
            await db.refresh(nuevo_horario)
            return nuevo_horario

    @put("/horarios/{horario_id}")
    async def actualizar_horario(self, horario_id: int, horario_data: dict):
        async with get_db_session() as db:
            result = await db.execute(select(Bloque).where(Bloque.bloque_id == horario_id))
            horario = result.scalars().first()
            
            if not horario:
                raise HTTPException(status_code=404, detail="Horario no encontrado")
            
            for key, value in horario_data.items():
                setattr(horario, key, value)
                
            await db.commit()
            await db.refresh(horario)
            return horario

    @delete("/horarios/{horario_id}")
    async def eliminar_horario(self, horario_id: int):
        async with get_db_session() as db:
            result = await db.execute(select(Bloque).where(Bloque.bloque_id == horario_id))
            horario = result.scalars().first()
            
            if not horario:
                raise HTTPException(status_code=404, detail="Horario no encontrado")
            
            await db.delete(horario)
            await db.commit()
            return {"mensaje": f"El horario con ID {horario_id} ha sido eliminado"}

    @get("/aulas")
    async def obtener_aulas(self):
        async with get_db_session() as db:
            result = await db.execute(select(Aula))
            return result.scalars().all()

    @get("/docentes")
    async def obtener_docentes(self):
        async with get_db_session() as db:
            result = await db.execute(select(Profesores))
            return result.scalars().all()