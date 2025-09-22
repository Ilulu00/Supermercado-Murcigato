"""
Entidad Productos
Modelo de Producto con SQLAlchemy y esquemas de validación con Pydantic.
"""

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


class Producto(Base):
    """
    Modelo de Producto que representa la tabla 'productos'

    Atributos:
        id_producto: Identificador único del producto
        nombre_producto: Nombre del producto
        precio_producto: Precio del producto
        stock: Cantidad en stock
        id_categoria: ID de la categoría a la que pertenece
        id_usuarioCrea: ID del usuario que creó el producto
        id_usuarioActual: ID del usuario que actualizo el producto.
        fecha_creacion: Fecha y hora de creación
        fecha_actualizacion: Fecha y hora de última actualización
    """

    __tablename__ = "Productos"

    id_producto = Column(UUID, primary_key=True, autoincrement=True)
    nombre_producto = Column(String(200), nullable=False, index=True)
    precio_producto = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    id_categoria = Column(UUID, ForeignKey("categorias.id"), nullable=False)
    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("Usuarios.id_usuario"), nullable=False
    )
    id_usuarioCrea = Column(UUID, ForeignKey("Usuario.id_usuario"), nullable=False)
    id_usuarioActual = Column(UUID, ForeignKey("Usuario.id_usuario"), nullable=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.now, nullable=True)

    categoria = relationship("Categoria", back_populates="productos")
    usuarioCreador = relationship(
        "Usuario", back_populates="productoCreado", foreign_keys=[id_usuario]
    )
    carritos = relationship("Detalle_carrito", back_populates="producto")

    usuario_crea = relationship(
        "Usuario",
        foreign_keys=[id_usuarioCrea],
        overlaps="usuario,usuario_edita,productos",
    )
    usuario_edita = relationship(
        "Usuario",
        foreign_keys=[id_usuarioActual],
        overlaps="usuario,usuario_crea,productos",
    )

    def __repr__(self):
        return (
            f"<ID Producto: {self.id_producto}\n"
            f"Nombre del producto: {self.nombre_producto}\n"
            f"Precio del producto: {self.precio_producto}\n"
            f"Cantidad actual: {self.stock}"
        )
