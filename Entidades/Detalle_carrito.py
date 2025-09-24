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

        id_detalle_carrito: identificador unico.
        id_carrito: Llave foranea que conecta al carrito con los detalles de los productos.
        id_producto: LLave foranea que conecte los productos y sus datos con el Detalle carrito
        cantidad: cuanta cantidad de x producto hay en el carrito.

    """

    __tablename__ = "Detalle_carrito"

    id_detalle = Column(UUID, primary_key=True, default=uuid4, nullable=False)
    id_carrito = Column(UUID, ForeignKey("Carrito.id_carrito"), nullable=False)
    id_producto = Column(UUID, ForeignKey("Productos.id_producto"), nullable=False)
    cantidad = Column(Integer, nullable=False)

    carrito = relationship("Carrito", back_populates="productos")
    producto = relationship("Producto", back_populates="carritos")

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
            "ID carrito": str(self.id_carrito),
            "Cliente": {
                "ID cliente": str(self.carritoUsuario.id_usuario),
                "Nombre Completo": f"{self.carritoUsuario.primer_nombre} {self.carritoUsuario.segundo_nombre or ''} "
                f"{self.carritoUsuario.primer_apellido} {self.carritoUsuario.segundo_apellido or ''}",
            },
            "Productos": [
                {
                    "ID producto": str(p.id_producto),
                    "Nombre": p.nombre_producto,
                    "Precio": p.precio_producto,
                }
                for p in self.carritoProducto
            ],
            "Precio total": self.Precio_total,
        }


class CarritoBase(BaseModel):
    id_usuario: str = Field(..., description="Usuario al que pertence el carrito.")
    id_producto: Optional[str] = Field(
        None, description="Producto que hace parte del carrito."
    )


class RespuestaCarrito(CarritoBase):

    id: int
    fecha_registro: datetime
    fecha_actul: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class ListaCarritos(BaseModel):

    carrito: List[RespuestaCarrito]
    total: int
    pagina: int
    por_pagina: int

    class Config:
        from_attributes = True
