"""
Esquemas pydantic para la respuesta de la API
"""

from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


class CarritoBase(BaseModel):
    id_usuario: UUID
    id_producto: UUID


class RespuestaCarrito(CarritoBase):

    id_carrito: UUID
    fecha_crea: datetime
    fecha_actul: Optional[datetime] = None

    class Config:
        from_attributes = True


class DetalleCarritoBase(BaseModel):
    id_carrito: UUID
    id_producto: UUID
    cantidad: int


class DetalleCarritoCreate(DetalleCarritoBase):
    pass


class DetalleCarritoResponse(DetalleCarritoBase):
    id: UUID
    subtotal: int

    class Config:
        orm_mode = True


class FacturaBase(BaseModel):
    id_factura: UUID
    metodo_pago: str
    subtotal: Optional[float]
    total: float
    descuento: Optional[float]
    id_carrito: UUID
    id_usuario: UUID
    fecha_creacion: datetime


class RespuestaFactura(FacturaBase):

    id_factura: UUID
    metodo_pago: str
    subtotal: Optional[float]
    total: float
    descuento: Optional[float]
    id_carrito: str
    id_usuario: str
    id_usuarioCrea: str
    fecha_creacion: datetime
    fecha_actul: Optional[datetime] = None

    class Config:
        from_attributes = True


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int
