from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models.base import Base

Base.metadata.create_all(bind=engine)

# Inicializar servidor fastAPI
app = FastAPI()

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
