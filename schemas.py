"""
Esquemas pydantic para la respuesta de la API
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr


class CarritoBase(BaseModel):
    id_usuario: UUID


class RespuestaCarrito(CarritoBase):

    id_carrito: UUID
    fecha_crea: datetime
    fecha_actual: Optional[datetime] = None

    class Config:
        from_attributes = True


class CrearCarrito(CarritoBase):
    pass


class DetalleCarritoBase(BaseModel):
    id_carrito: UUID
    id_producto: UUID
    cantidad: int


class DetalleCarritoCreate(DetalleCarritoBase):
    pass


class DetalleCarritoResponse(DetalleCarritoBase):
    subtotal: int

    class Config:
        from_attributes = True


class FacturaBase(BaseModel):
    id_factura: UUID
    metodo_pago: str
    subtotal: Optional[float]
    total: float
    descuento: Optional[float]
    id_carrito: UUID
    id_usuario: UUID
    fecha_creacion: datetime


class CrearFactura(FacturaBase):
    pass


class RespuestaFactura(FacturaBase):

    id_factura: UUID
    fecha_actual: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioConCarrito(UsuarioResponse):
    carrito: RespuestaCarrito


class CarritoConFactura(RespuestaCarrito):
    factura: RespuestaFactura


class CarritoConDetalles(RespuestaCarrito):
    detalles: List[DetalleCarritoResponse] = []


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int
