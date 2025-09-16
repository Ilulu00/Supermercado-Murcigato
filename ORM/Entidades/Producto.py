"""
Entidad Producto
================

Modelo de Producto con SQLAlchemy y esquemas de validación con Pydantic.
"""
from typing import Any

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.config import Base

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
    __tablename__ = "Productos"
    
    id_producto = Column(UUID, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(200), nullable=False, index=True)
    precio_producto = Column(Float, nullable=False)
    stock_producto = Column(Integer, default=0, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    
    #Claves foraneas
    id_categoria= Column(Integer, ForeignKey("Categoria.id_categoria"), nullable=False)

    #Campos auditoria
    id_usuario_crea = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable=False)
    id_usuario_edita = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable = False)

    # Relaciones
    categoria = relationship("Categoria", back_populates="productos")

    #Relaciones auditoria
    usuario_crea = relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="Usuario,usuario_edita")
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="Usuario,usuario_crea")

    def __repr__(self):
        return f"<Producto(id_producto={self.id_producto}, nombre='{self.nombre}', precio={self.precio}, stock={self.stock_producto})>"