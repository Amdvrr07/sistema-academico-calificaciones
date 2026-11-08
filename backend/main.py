from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers import (
  #  aulas,
    auth,
  #  calificaciones,
   # horarios,
    inscripcion,
    materias,
    notas,
    #reportes,
)

# Inicializar servidor fastAPI
app = FastAPI()
app.include_router(inscripcion.router)
app.include_router(materias.router)
app.include_router(notas.router)
#app.include_router(horarios.router)
#app.include_router(aulas.router)
#app.include_router(calificaciones.router)
#app.include_router(reportes.router)
app.include_router(auth.router)


origenes = [
    "http://localhost:3000", # Puerto del frontend
    "http://localhost:8000" # Puerto del backend
]

# Agregar el middleware del sistema
app.add_middleware(
    CORSMiddleware, # Habilita el Intercambio de Recursos de Origen Cruzado(CORS)
    allow_origins=origenes, # Especifica la ruta los puertos
    allow_methods= ["*"] # Permite todos los métodos del backend
)
