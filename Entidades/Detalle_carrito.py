"""
Modelo de la entidad DetalleCarrito.
Aqui sera donde se creara la entidad carritocon SQLalchemy, asi como algunas validaciones con pydantic
"""

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.config import Base


class Detalle_carrito(Base):
    """
    Modelo de los detalles de un carro de compras, donde se podran guardar mas de 1 producto.

        id_detalle: identificador unico.
        id_carrito: Llave foranea que conecta al carrito con los detalles de los productos.
        id_producto: LLave foranea que conecte los productos y sus datos con el Detalle carrito
        cantidad: cuanta cantidad de x producto hay en el carrito.

    """

    __tablename__ = "Detalle_carrito"

    id_detalle = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    id_carrito = Column(
        UUID(as_uuid=True), ForeignKey("Carrito.id_carrito"), nullable=False
    )
    id_producto = Column(
        UUID(as_uuid=True), ForeignKey("Productos.id_producto"), nullable=False
    )
    cantidad = Column(Integer, nullable=False)

    carrito = relationship(
        "Carrito", back_populates="detalles", foreign_keys=[id_carrito]
    )
    producto = relationship(
        "Producto", back_populates="detalles", foreign_keys=[id_producto]
    )

    @property
    def nombre_producto(self):
        return self.producto.nombre_producto

    @property
    def precio_producto(self):
        return self.producto.precio_producto

    @property
    def subtotal(self):
        return self.cantidad * self.producto.precio_producto

    def __repr__(self):
        return (
            f"<Detalle de carrito número: {self.id_detalle}.\n"
            f"Carrito: {self.carrito.id_carrito}\n."
            f"Producto: {self.id_producto}"
            f"Subtotal: {self.subtotal}"
        )

    def to_dict(self):
        return {
            "ID detalle": str(self.id_detalle),
            "ID carrito": str(self.id_carrito),
            "Producto": {
                "ID": str(self.producto.id_producto),
                "Nombre": self.producto.nombre_producto,
                "Precio unitario": self.producto.precio_producto,
            },
            "Cantidad": self.cantidad,
            "Subtotal": self.subtotal,
        }


from Entidades.Producto import Producto
