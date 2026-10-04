from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import backend.models as _models
from backend.exceptions import Conflicto, NoEncontrado
from backend.database import engine
from backend.routes.inscripcion import router as inscripciones_router
from backend.routes.materias import router as materias_router
from backend.routes.notas import router as notas_router

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await engine.dispose()


app = FastAPI(title="Sistema de Gestión Escolar", lifespan=lifespan)

app.include_router(materias_router)
app.include_router(notas_router)
app.include_router(inscripciones_router)


@app.exception_handler(NoEncontrado)
async def manejar_no_encontrado(request: Request, exc: NoEncontrado):
    return JSONResponse(status_code=404, content={"detail": exc.detalle})


@app.exception_handler(Conflicto)
async def manejar_conflicto(request: Request, exc: Conflicto):
    return JSONResponse(status_code=409, content={"detail": exc.detalle})


@app.get("/", tags=["Inicio"])
async def saludo():
    return {"message": "Sistema de Gestión Escolar: API en línea"}
