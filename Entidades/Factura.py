"""
Modelo de la entidad Factura.
Aqui sera donde se creara la entidad Factura con SQLalchemy, asi como algunas validaciones con pydantic
"""

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.config import Base


class Factura(Base):
    """
    Modelo de las columnas que haran parte de la clase factura, la cual servira como base para crear, y posterior mostrar esta factura.

        id_factura: El identificador único de cada factura
        metodo_pago: con que metodo pago el usuario
        subtotal_total: el total de los productos sin descuento
        total: el total de los productos con descuento
        activo: muestra si la factura ya se cancelo o sigue vigente de pago
        descuento: Si al final se aplico un descuento o no, siguiendo ciertas reglas.
        id_carrito: Para mostrar los productos que se compro.
    """

    __tablename__ = "Factura"

    id_factura = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    metodo_pago = Column(String, nullable=False)
    subtotal_total = Column(Float, nullable=True)
    descuento = Column(Float, nullable=True)
    total = Column(Float, nullable=True)
    activo = Column(Boolean, nullable=False)
    id_carrito = Column(
        UUID(as_uuid=True), ForeignKey("Carrito.id_carrito"), nullable=False
    )
    id_usuario = Column(
        UUID(as_uuid=True), ForeignKey("Usuarios.id_usuario"), nullable=False
    )
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)

    carritoF = relationship("Carrito", back_populates="facturaC")
    usuarioF = relationship(
        "Usuario", back_populates="facturaU", foreign_keys=[id_usuario]
    )

    def __repr__(self):
        return (
            f"Factura {self.id_factura}\n"
            f"Cliente: {self.usuarioF.id_usuario}\n"
            f"Carrito: {self.carritoF.id_carrito}\n"
            f"Metodo de pago: {self.metodo_pago}\n"
            f"Subtotal: {self.subtotal_total}\n"
            f"Total: {self.total}\n"
            f"Descuento aplicado: {self.descuento}"
            f"Estado: {self.activo}\n"
        )

    def to_dict(self):
        return {
            "ID Factura": str(self.id_factura),
            "Cliente": {
                "ID cliente": str(self.carritoF.id_usuario),
                "Nombre Completo": f"{self.usuarioF.primer_nombre} {self.usuarioF.segundo_nombre or ''} "
                f"{self.usuarioF.primer_apellido} {self.usuarioF.segundo_apellido or ''}",
            },
            "Carrito": {
                "ID Carrito": str(self.carritoF.id_carrito),
                "Productos": [
                    {
                        "ID producto": str(dc.producto.id_producto),
                        "Nombre": dc.producto.nombre_producto,
                        "Precio": dc.producto.precio_producto,
                    }
                    for dc in self.carritoF.productos
                ],
                "Metodo de pago": self.metodo_pago,
                "Subtotal": self.subtotal_total,
                "Total": self.total,
                "Descuento": self.descuento,
            },
        }
