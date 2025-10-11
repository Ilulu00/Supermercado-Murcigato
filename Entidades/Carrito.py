"""
Modelo de la entidad Carrito.
Aqui sera donde se creara la entidad carritocon SQLalchemy, asi como algunas validaciones con pydantic
"""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Boolean
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

    id_carrito = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("Usuarios.id_usuario"), nullable=False
    )
    fecha_crea = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actual = Column(DateTime, onupdate=datetime.now)
    activo = Column(Boolean, default=True, nullable=False)

    carritoUsuario = relationship(
        "Usuario", back_populates="usuarioCarrito", foreign_keys=[id_usuario]
    )
    detalles = relationship(
        "Detalle_carrito",
        back_populates="carrito",
        foreign_keys="Detalle_carrito.id_carrito",
        cascade="all, delete-orphan",
    )
    facturaC = relationship("Factura", back_populates="carritoF")

    @property
    def total(self):
        if not self.detalles:
            return 0.0
        return sum(detalle.subtotal for detalle in self.detalles)

    def __repr__(self):
        return (
            f"<Carrito(id_carrito={self.id_carrito}, "
            f"id_usuario={self.id_usuario}, "
            f"total={self.total}, activo={self.activo})>"
        )

    def to_dict(self):
        return {
            "ID carrito": str(self.id_carrito),
            "Activo": self.activo,
            "Cliente": {
                "ID usuario": str(self.carritoUsuario.id_usuario),
                "Nombre completo": f"{self.carritoUsuario.primer_nombre} {self.carritoUsuario.segundo_nombre or ''} "
                f"{self.carritoUsuario.primer_apellido} {self.carritoUsuario.segundo_apellido or ''}".strip(),
                "Correo": self.carritoUsuario.correo,
            },
            "Fecha de creación": (
                self.fecha_crea.isoformat() if self.fecha_crea else None
            ),
            "Última actualización": (
                self.fecha_actual.isoformat() if self.fecha_actual else None
            ),
            "Productos": [
                {
                    "ID detalle": str(d.id_detalle),
                    "ID producto": str(d.producto.id_producto),
                    "Nombre": d.producto.nombre_producto,
                    "Precio unitario": d.producto.precio_producto,
                    "Cantidad": d.cantidad,
                    "Subtotal": d.subtotal,
                }
                for d in self.detalles
            ],
            "Total a pagar": (
                sum(d.subtotal for d in self.detalles) if self.detalles else 0.0
            ),
        }
