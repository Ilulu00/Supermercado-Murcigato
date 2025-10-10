"""
Entidad Productos
Modelo de Producto con SQLAlchemy
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

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
        fecha_creacion: Fecha y hora de creación
        fecha_actualizacion: Fecha y hora de última actualización
    """

    __tablename__ = "Productos"

    id_producto = Column(UUID, primary_key=True, default=uuid4, nullable=False)
    nombre_producto = Column(String(200), nullable=False, index=True)
    precio_producto = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    id_categoria = Column(UUID, ForeignKey("Categorias.id_categoria"), nullable=False)
    id_proveedor = Column(UUID, ForeignKey("Proveedor.id_proveedor"), nullable=False)

    fecha_creacion = Column(DateTime, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.now, nullable=True)

    categoria = relationship(
        "Categoria", back_populates="productos", foreign_keys=[id_categoria]
    )
    proveedor = relationship(
        "Proveedor", back_populates="productos", foreign_keys=[id_proveedor]
    )
    detalles = relationship("Detalle_carrito", back_populates="producto")


def __repr__(self):
    return (
        f"<ID Producto: {self.id_producto}\n"
        f"Nombre del producto: {self.nombre_producto}\n"
        f"Precio del producto: {self.precio_producto}\n"
        f"Cantidad actual: {self.stock}"
    )


from Entidades.Categoria_prod import Categoria
from Entidades.Detalle_carrito import Detalle_carrito
