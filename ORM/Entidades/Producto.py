"""
Entidad Producto
================

Modelo de Producto con SQLAlchemy y esquemas de validación con Pydantic.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from ..database.database import Base

class Producto(Base):
    """
    Modelo de Producto que representa la tabla 'productos'
    
    Atributos:
        id_producto: Identificador único del producto
        nombre_producto: Nombre del producto
        precio_producto: Precio del producto
        stock_producto: Cantidad en stock
        id_categoria: ID de la categoría a la que pertenece
        id_usuario: ID del usuario que creó el producto
        fecha_creacion: Fecha y hora de creación
        fecha_actualizacion: Fecha y hora de última actualización
    """
    __tablename__ = 'productos'
    
    id_producto = Column(UUID, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(200), nullable=False, index=True)
    precio_producto = Column(Float, nullable=False)
    stock_producto = Column(Integer, default=0, nullable=False)
    id_categoria= Column(UUID, ForeignKey('categorias.id'), nullable=False)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relaciones
    categoria = relationship("Categoria", back_populates="productos")
    usuario = relationship("Usuario", back_populates="productos")