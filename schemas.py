"""
Esquemas pydantic para la respuesta de la API
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr


# Schemas de usuario
class UsuarioBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    telefono: Optional[str] = None
    correo: str
    activo: bool
    fecha_registro: datetime
    es_admin: bool = False


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    activo: Optional[bool] = None
    es_admin: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    activo: bool
    fecha_registro: datetime
    fecha_actual: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioListResponse(BaseModel):
    data: List[UsuarioResponse]
    totalPages: int
    currentPage: int
    totalItems: int
    size: int

    class Config:
        from_attributes = True


# Schemas de carrito y detalles_carrito
class CarritoBase(BaseModel):
    id_usuario: UUID
    fecha_crea: datetime
    fecha_actual: Optional[datetime] = None
    activo: bool


class CrearCarrito(BaseModel):
    id_usuario: UUID
    activo: bool


class RespuestaCarrito(CarritoBase):
    id_carrito: UUID
    id_usuario: UUID
    fecha_crea: datetime
    fecha_actual: Optional[datetime] = None
    activo: bool

    class Config:
        from_attributes = True


class DetalleCarritoBase(BaseModel):
    id_carrito: UUID
    id_producto: UUID
    cantidad: int


class DetalleCarritoCreate(DetalleCarritoBase):
    id_detalle: UUID


class DetalleCarritoUpdate(BaseModel):
    cantidad: int


class DetalleCarritoResponse(DetalleCarritoBase):
    id_detalle: UUID
    precio_producto: float
    subtotal: float

    class Config:
        from_attributes = True


class DetalleCarritoOut(BaseModel):
    id_detalle: UUID
    id_producto: UUID
    nombre_producto: str
    cantidad: int
    precio_producto: float
    subtotal: float


class CarritoOut(BaseModel):
    id_carrito: UUID
    id_usuario: UUID
    fecha_crea: datetime
    activo: bool
    detalles: List[DetalleCarritoOut]
    subtotal_general: float

    class Config:
        from_attributes = True


class CarritoListResponse(BaseModel):
    data: List[CarritoOut]
    totalPages: int
    currentPage: int
    totalItems: int
    size: int

    class Config:
        from_attributes = True


# Schemas de factura
class FacturaBase(BaseModel):
    id_usuario: UUID
    id_carrito: UUID
    activo: bool
    metodo_pago: str
    subtotal_total: float
    descuento: Optional[float]
    total: float


class CrearFactura(FacturaBase):
    pass


class DetalleFacturaRespuesta(BaseModel):
    nombre_producto: str
    cantidad: int
    precio_producto: float
    subtotal: float

    class config:
        from_attributes = True


class RespuestaFactura(FacturaBase):
    id_factura: UUID
    fecha_creacion: datetime
    detalles: List[DetalleFacturaRespuesta]

    class Config:
        from_attributes = True


class FacturaListResponse(BaseModel):
    data: List[RespuestaFactura]
    totalPages: int
    currentPage: int
    totalItems: int
    size: int

    class Config:
        from_attributes = True


# Schemas de categoria
class CategoriaBase(BaseModel):
    nombre_categoria: str
    descripcion: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre_categoria: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_edicion: Optional[datetime] = None


class CategoriaResponse(CategoriaBase):
    id_categoria: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoriaListResponse(BaseModel):
    data: List[CategoriaResponse]
    totalPages: int
    currentPage: int
    totalItems: int
    size: int

    class Config:
        from_attributes = True


# Schemas de producto
class ProductoBase(BaseModel):
    nombre_producto: str
    precio_producto: float
    stock: int
    id_categoria: UUID
    id_proveedor: UUID
    fecha_creacion: datetime


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre_producto: Optional[str] = None
    precio_producto: Optional[float] = None
    stock: Optional[int] = None
    id_categoria: Optional[UUID] = None
    fecha_actualizacion: Optional[datetime]


class ProductoResponse(ProductoBase):
    id_producto: UUID
    fecha_actualizacion: Optional[datetime] = None
    categoria: Optional[dict] = None

    class Config:
        from_attributes = True


class ProductoListResponse(BaseModel):
    data: List[ProductoResponse]
    totalPages: int
    currentPage: int
    totalItems: int
    size: int

    class Config:
        from_attributes = True


# Schemas de proveedor
class ProveedorBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    telefono: Optional[str] = None
    correo: str
    fecha_creacion: datetime


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None


class ProveedorResponse(ProveedorBase):
    id_proveedor: UUID
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProveedorListResponse(BaseModel):
    data: List[ProveedorResponse]
    totalPages: int
    currentPage: int
    totalItems: int
    size: int

    class Config:
        from_attributes = True


# Schemas de relaciones
class ProductoConCategoria(ProductoResponse):
    categoria: CategoriaResponse


class UsuarioConProductos(UsuarioResponse):
    productos: list[ProductoResponse] = []


class CategoriaConProductos(CategoriaResponse):
    productos: list[ProductoResponse] = []


class ProductoConProveedor(ProductoResponse):
    proveedor: list[ProveedorResponse] = []


class UsuarioConCarrito(UsuarioResponse):
    carrito: RespuestaCarrito


class CarritoConFactura(RespuestaCarrito):
    factura: RespuestaFactura


class CarritoConDetalles(RespuestaCarrito):
    detalles: List[DetalleCarritoResponse] = []

    class Config:
        from_attributes = True


# Schemas del API
class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int
