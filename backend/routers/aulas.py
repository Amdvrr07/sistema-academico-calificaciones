from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.controllers.aula import (
    actualizar_aula,
    crear_aula,
    eliminar_aula,
    listar_aulas,
    obtener_aula,
)
from backend.database import get_db
from backend.schemas.aula import AulaCreate, AulaRead, AulaUpdate

router = APIRouter(prefix="/aulas", tags=["Aulas"])

@router.post("/", response_model=AulaRead, status_code=201)
def crear(datos: AulaCreate, db: Session = Depends(get_db)):
    """Registra una nueva aula en el sistema."""
    aula = crear_aula(db, datos)
    if aula is None:
        raise HTTPException(status_code=409, detail=f"Ya existe un aula con el código [{datos.codigo}]")
    return aula

@router.get("/", response_model=list[AulaRead])
def listar(db: Session = Depends(get_db)):
    return listar_aulas(db)

@router.get("/{aula_id}", response_model=AulaRead)
def obtener(aula_id: int, db: Session = Depends(get_db)):
    aula = obtener_aula(db, aula_id)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula

@router.put("/{aula_id}", response_model=AulaRead)
def actualizar(aula_id: int, datos: AulaUpdate, db: Session = Depends(get_db)):
    aula = actualizar_aula(db, aula_id, datos)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return aula

@router.delete("/{aula_id}")
def eliminar(aula_id: int, db: Session = Depends(get_db)):
    aula = eliminar_aula(db, aula_id)
    if aula is None:
        raise HTTPException(status_code=404, detail="Aula no encontrada")
    return {"mensaje": f"El aula con ID {aula_id} ha sido eliminada"}
