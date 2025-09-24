"""
Entidad Productos
Modelo de Producto con SQLAlchemy
"""
from typing import Any


from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    ForeignKey,
)
from database.config import Base
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.config import Base


class Producto(Base):
    """
    Modelo de Producto que representa la tabla 'productos'

    Atributos:
        id_producto: Identificador unico del producto
        nombre_producto: Nombre del producto
        precio_producto: Precio del producto
        stock: Cantidad en stock
        id_categoria: ID de la categoria a la que pertenece
        id_proveedor: ID del provedor del producto
        id_usuarioCrea: ID del usuario que creó el producto
        id_usuarioActualiza: ID del usuario que actualizo el producto.
        fecha_creacion: Fecha y hora de creación
        fecha_actualizacion: Fecha y hora de última actualización
    """

    __tablename__ = "Productos"

    id_producto = Column(UUID, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(200), nullable=False, index=True)
    precio_producto = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    id_proveedor = Column(UUID(as_uuid=True), ForeignKey=("Proveedor.id_proveedor"), nullable=False)
    id_categoria = Column(UUID, ForeignKey("categorias.id"), nullable=False)
    id_proveedor = Column(UUID, ForeignKey("proveedor.id", nullable=False))

    id_usuarioCrea = Column(UUID, ForeignKey("Usuario.id_usuario"), nullable=False)
    id_usuarioActualiza = Column(UUID, ForeignKey("Usuario.id_usuario"), nullable=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.now, nullable=True)

    categoria = relationship("Categoria", back_populates="productos")

    proveedor = relationship("Proveedor", back_populates="productos")
    carritos = relationship("Detalle_carrito", back_populates="productos")

    usuario_crea = relationship(
        "Usuario",
        foreign_keys=[id_usuarioCrea],
        overlaps="usuario,usuario_crea,productos",
    )
    usuario_Actualiza = relationship(
        "Usuario",
        foreign_keys=[id_usuarioActualiza],
        overlaps="usuario,usuario_Actualiza,productos",
    )

    def __repr__(self):
        return (
            f"<ID Producto: {self.id_producto}\n"
            f"Nombre del producto: {self.nombre_producto}\n"
            f"Precio del producto: {self.precio_producto}\n"
            f"Cantidad actual: {self.stock}"
        )

    __tablename__ = "Productos"
    
    id_producto = Column(UUID, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(200), nullable=False, index=True)
    precio_producto = Column(Float, nullable=False)
    stock_producto = Column(Integer, default=0, nullable=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    
    id_categoria= Column(Integer, ForeignKey("Categoria.id_categoria"), nullable=False)

    id_usuario_crea = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable=False)
    id_usuario_edita = Column(Integer, ForeignKey("Usuario.id_usuario"), nullable = False)

    categoria = relationship("Categoria", back_populates="productos")

    usuario_crea = relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="Usuario,usuario_edita")
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="Usuario,usuario_crea")

    def __repr__(self):
        return f"<Producto(id_producto={self.id_producto}, nombre='{self.nombre}', precio={self.precio}, stock={self.stock_producto})>"

