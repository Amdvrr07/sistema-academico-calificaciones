from sqlalchemy import String, ForeignKey, Date, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date
from typing import List

class Representante(Base):
    __tablename__ = "representantes"

    representante_id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    cedula: Mapped[str] = mapped_column(String(10), unique=True)
    correo: Mapped[str] = mapped_column(String(100), unique=True)
    telefono: Mapped[str] = mapped_column(String(20))
    direccion: Mapped[str] = mapped_column(String(200))
    
    alumnos: Mapped[List["Alumnos"]] = relationship(back_populates="representante", cascade="all, delete-orphan")

class Alumnos(Base):
    __tablename__ = "alumnos"

    alumno_id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    cedula: Mapped[str] = mapped_column(String(10), unique=True)
    fecha_nacimiento: Mapped[date] = mapped_column(Date) # Cambiado a Date
    
    representante_id: Mapped[int] = mapped_column(ForeignKey("representantes.representante_id"))
    representante: Mapped["Representante"] = relationship(back_populates="alumnos")
    curso_id: Mapped[int] = mapped_column(ForeignKey("cursos.curso_id"))

class Profesores(Base):
    __tablename__ = "profesores"

    profesor_id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    cedula: Mapped[str] = mapped_column(String(10), unique=True)
    telefono: Mapped[str] = mapped_column(String(20))
    correo: Mapped[str] = mapped_column(String(100), unique=True)
    especialidad: Mapped[str] = mapped_column(String(20))
    
    salario_base: Mapped[float] = mapped_column(
        Numeric(8, 2),
        CheckConstraint("salario_base > 0", name="check_salario_base")
    )
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.usuario_id"), unique=True)