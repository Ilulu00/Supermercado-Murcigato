"""
Esquemas pydantic para la respuesta de la API
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    primerNombre: str
    segundoNombre: Optional[str] = None
    primerApellido: str
    segundoApellido: Optional[str] = None
    direccion: str
    telefono: Optional[str] = None
    correo: str
    telefono: Optional[str] = None
    contraseña: str
    rol: str
    activo: bool


class UsuarioCreate(UsuarioBase):
    id_usuario: UUID
    primer_nombre: str
    primer_apellido: str
    correo: str
    contraseña: str
    direccion: str
    segundo_nombre: Optional[str] = None
    segundo_apellido: Optional[str] = None
    telefono: Optional[str] = None
    rol: str = "Cliente"


class UsuarioUpdate(BaseModel):
    primerNombre: Optional[str] = None
    segundoNombre: Optional[str] = None
    primerApellido: Optional[str] = None
    segundoApellido: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None
    rol: Optional[str] = "Cliente"
    activo: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id_usuario: UUID
    activo: bool
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioLogin(BaseModel):
    correo: str
    contraseña: str


class CambioContraseña(BaseModel):
    contraseña_actual: str
    nueva_contraseña: str


class loginResponse(BaseModel):
    contraseña: str
    correo: UsuarioResponse


class CarritoBase(BaseModel):
    id_usuario: UUID
    id_usuario: UUID
    fecha_crea: datetime
    fecha_actual: Optional[datetime] = None


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
    id_usuario: UUID
    id_carrito: UUID
    metodo_pago: str
    subtotal: Optional[float]
    descuento: Optional[float]
    total: float
    fecha_creacion: datetime


class CrearFactura(FacturaBase):
    pass


class RespuestaFactura(FacturaBase):

    id_factura: UUID
    fecha_actual: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoriaBase(BaseModel):
    id_categoria: UUID
    nombre: str
    descripcion: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class CategoriaResponse(CategoriaBase):
    id_categoria: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductoBase(BaseModel):
    id_producto: UUID
    nombre: str
    precio: float
    stock: int
    categoria_id: UUID
    usuario_id: UUID


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None
    categoria_id: Optional[UUID] = None
    usuario_id: Optional[UUID] = None


class ProductoResponse(ProductoBase):
    id_producto: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProveedorBase(BaseModel):
    id_proveedor: UUID
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    telefono: Optional[str] = None
    correo: str


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(BaseModel):
    primerNombre: Optional[str] = None
    segundoNombre: Optional[str] = None
    primerApellido: Optional[str] = None
    segundoApellido: Optional[str] = None
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = None


class ProveedorResponse(ProveedorBase):
    id_proveedor: UUID
    fecha_creacion: datetime
    fecha_edicion: Optional[datetime] = None

    class Config:
        from_attributes = True


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


class RespuestaAPI(BaseModel):
    mensaje: str
    exito: bool = True
    datos: Optional[dict] = None


class RespuestaError(BaseModel):
    mensaje: str
    exito: bool = False
    error: str
    codigo: int
