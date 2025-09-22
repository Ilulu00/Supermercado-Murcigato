"""
Modelo de la entidad Carrito.
Aqui sera donde se creara la entidad carritocon SQLalchemy, asi como algunas validaciones con pydantic
"""

from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import uuid4, UUID


class Carrito(Base):
    """
    Modelo de un carro de compras, la cual sera una tabla.

        id_carrito: identificador unico.
        id_usuario: El id del usuario al q pertenece el carrito de compras

    """

    __tablename__ = "Carrito"

    id_carrito = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    id_detalle = Column(
        UUID(as_uuid=True), ForeignKey("Detalle_carrito.id_detalle"), nullable=False
    )
    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("Usuario.id_usuario"), nullable=False
    )
    fecha_crea = Column(DateTime, default=datetime.now)
    fecha_actul = Column(DateTime, onupdate=datetime.now)

    carritoUsuario = relationship("Usuario", back_populates="usuarioCarrito")
    productos = relationship("Detalle_carrito", back_populates="carrito")
    facturaC = relationship("Factura", back_populates="carritoF")

    @property
    def total(self):
        return sum(self.productos.subtotal)

    def __repr__(self):
        return (
            f"<Carrito de compras {self.id_carrito}.\n"
            f"ID del cliente: {self.carritoUsuario.id_usuario}\n"
            f"Cantidad de productos: {len(self.productos)}"
            f"Total a pagar: {self.precio_total}>"
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
            "Precio total": self.total,
        }


class CarritoBase(BaseModel):
    id_usuario: UUID = Field(..., description="Usuario al que pertence el carrito.")
    id_producto: Optional[UUID] = Field(
        None, description="Producto que hace parte del carrito."
    )


class RespuestaCarrito(CarritoBase):

    id: int
    fecha_crea: datetime
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
