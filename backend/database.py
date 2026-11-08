import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

# Variables de entorno del contenedor de Docker
"""
host = os.getenv("POSTGRES_HOST", "localhost")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "root_password")
db = os.getenv("POSTGRES_DB", "database")
port = os.getenv("POSTGRES_PORT", "5432")
"""

load_dotenv() 
user = os.getenv("DB_USER", "localhost")
password = os.getenv("DB_PASSWORD", "root_password")
port = os.getenv("DB_PORT", "5432")
db = os.getenv("DB_NAME", "database")
host = os.getenv("DB_HOST", "localhost")

# Enlace para la conexión con la base de datos. asyncpg es un driver asíncrono para PostgreSQL
DB_URL = os.getenv(
    "DATABASE_URL", 
    f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
)

DB_URL = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"

# Actua como puerto de entrada y base de conexiones entre la base de datos y el backend en Python
engine = create_async_engine(DB_URL, echo=True)
SYNC_DB_URL = DB_URL.replace("+asyncpg", "+psycopg2")
sync_engine = create_engine(SYNC_DB_URL, echo=True)

# Creación de sesión asíncrona, la cual gestiona operaciones de lectura y escritura, así como las transacciones
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
SyncSessionLocal = sessionmaker(bind=sync_engine, class_=Session, expire_on_commit=False)

#def get_db():
   # with SyncSessionLocal() as db:
  #      yield db

# Función generadora de sesión en la base de datos
async def get_db_session():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()