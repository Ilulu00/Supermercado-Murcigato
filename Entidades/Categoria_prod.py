"""
Entidad Categorias
Módelo de categorias con SQLAlchemy.
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.config import Base


class Categoria(Base):
    """
    Modelo de Categoria que representa la tabla 'Categorias'

    Atributos:
        id_cateoria: Identificador único del producto
        nombre_categoria: Nombre de la categoria
        descripción: Descripcion de cada categoria
        fecha_creacion: Fecha y hora de creación
        fecha_actualizacion: Fecha y hora de última actualización
    """

    __tablename__ = "Categorias"

    id_categoria = Column(UUID, primary_key=True, default=uuid4, index=True)
    nombre_categoria = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)

    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.now)

    productos = relationship("Producto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(id_categoria={self.id_categoria}, nombre='{self.nombre_categoria}')>"
