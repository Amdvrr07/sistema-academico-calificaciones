from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Variables de entorno del contenedor de Docker
host = os.getenv("POSTGRES_HOST", "localhost")
user = os.getenv("POSTGRES_USER", "postgres")
password = os.getenv("POSTGRES_PASSWORD", "root_password")
db = os.getenv("POSTGRES_DB", "database")
port = os.getenv("POSTGRES_PORT", "5432")

# Enlace para la conexión con la base de datos. psycopg2 es un driver para PostgreSQL
db_url = os.getenv(
    "DATABASE_URL", 
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
)

# Actua como puerto de entrada y base de conexiones entre la base de datos y el backend en Python
engine = create_engine(db_url, echo=True)

# Creación de sesión, la cual gestiona operaciones de lectura y escritura, así como las transacciones
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Función generadora de sesión en la base de datos
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()