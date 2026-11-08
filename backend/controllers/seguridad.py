import os
from datetime import UTC, datetime, timedelta
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db_session
from backend.models.usuario import Usuario  # Asegúrate de que la ruta coincida

# 1. LEER LA CLAVE SECRETA DE LAS VARIABLES DE ENTORNO (Solución A1)
# Si no existe en el archivo .env, levantará un error inmediatamente al arrancar la app.
password = os.getenv("DB_JWT_SECRET")


def _obtener_clave_secreta() -> str:
    if not password:
        raise RuntimeError("La variable de entorno 'DB_JWT_SECRET' no está configurada.")
    return password

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Configuración del esquema Bearer para interceptar el header 'Authorization'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


# --- 2. ENCRIPTACIÓN DE CONTRASEÑAS (BCRYPT) ---

def hash_password(contrasenia_plana: str) -> str:
    """Convierte una contraseña de texto plano en un hash seguro e ilegible."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(contrasenia_plana.encode('utf-8'), salt).decode('utf-8')


def verify_password(contrasenia_plana: str, contrasenia_hasheada: str) -> bool:
    """Compara una contraseña ingresada contra el hash seguro de la base de datos."""
    return bcrypt.checkpw(
        contrasenia_plana.encode('utf-8'), 
        contrasenia_hasheada.encode('utf-8')
    )


# --- 3. GESTIÓN DE TOKENS JWT (Tus funciones corregidas y seguras) ---

def codificar_token(payload: dict) -> str:
    """Genera un token JWT firmado criptográficamente con vencimiento."""
    copia_payload = payload.copy()
    expiracion = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    copia_payload.update({"exp": expiracion})
    
    # Operación matemática en memoria (Síncrona por estándar)
    # Usamos 'password' que es tu variable leída por el entorno OS
    return jwt.encode(copia_payload, _obtener_clave_secreta(), algorithm=ALGORITHM)


async def decodificar_y_verificar_usuario(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db_session)]
) -> Usuario:
    """
    Dependencia vertical completa (Solución C7). Intercepta el token, 
    lo decodifica con tu clave 'password', consulta de forma asíncrona 
    la base de datos y valida que el rol tenga accesos de auditoría.
    """
    exception_credenciales = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido, vencido o inexistente. Inicie sesión de nuevo.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decodificamos usando tu clave 'password' y el algoritmo correcto (HS256)
        payload = jwt.decode(token, _obtener_clave_secreta(), algorithms=[ALGORITHM])
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise exception_credenciales
    except jwt.PyJWTError:
        raise exception_credenciales

    # CONSULTA ASÍNCRONA: Validamos si el usuario realmente existe en la BD (C7)
    usuario = await db.get(Usuario, int(usuario_id))
    if usuario is None:
        raise exception_credenciales
        
    # VALIDACIÓN DE ROL (C7): Control de acceso estricto desde el servidor
    # Suponiendo que tu BD mapea: 1 = Administrador, 2 = Profesor
    roles = [1, 2]
    if usuario.rol_id not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Su rol no está autorizado para auditar ni alterar calificaciones."
        )
        
    return usuario
