"""
Modelo de la entidad Carrito.
Aqui sera donde se creara la entidad carritocon SQLalchemy, asi como algunas validaciones con pydantic
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.config import Base


class Carrito(Base):
    """
    Modelo de un carro de compras, la cual sera una tabla.

        id_carrito: identificador unico.
        id_usuario: El id del usuario al q pertenece el carrito de compras

    """

    __tablename__ = "Carrito"

    id_carrito = Column(UUID, primary_key=True, default=uuid4, nullable=False)
    id_usuario = Column(UUID, ForeignKey("Usuarios.id_usuario"), nullable=False)
    fecha_crea = Column(DateTime, default=datetime.now)
    fecha_actual = Column(DateTime, onupdate=datetime.now)

    carritoUsuario = relationship(
        "Usuario", back_populates="usuarioCarrito", foreign_keys=[id_usuario]
    )
    detalles = relationship(
        "Detalle_carrito",
        back_populates="carrito",
        foreign_keys="Detalle_carrito.id_carrito",
        cascade="all, delete-orphan",
    )
    facturaC = relationship("Factura", back_populates="carritoF", foreign_keys=[])

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
