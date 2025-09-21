"""
Modelo de la entidad Factura.
Aqui sera donde se creara la entidad Factura con SQLalchemy, asi como algunas validaciones con pydantic
"""
from sqlalchemy import Column, Float,String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from uuid import uuid4, UUID

Base = declarative_base()

class Factura (Base):
    """
    Modelo de las columnas que haran parte de la clase factura, la cual servira como base para crear, y posterior mostrar esta factura.
    
        id_factura: El identificador único de cada factura
        metodo_pago:
        subtotal:
        total:
        descuento: Si al final se aplico un descuento o no, siguiendo ciertas reglas.
        id_carrito: Para mostrar los productos que se compro.      
    """
    
    __tablename__ = 'Factura'
    
    id_factura = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    metodo_pago = Column(String, nullable=False)
    subtotal = Column(Float, nullable=True)
    total = Column(Float, nullable=True)
    descuento = Column(Float, nullable=True)
    id_carrito= Column(UUID(as_uuid=True), ForeignKey("Carrito.id_carrito"), nullable=False)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("Usuario.id_usuario"), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    id_usuarioCrea = Column(UUID, ForeignKey("Usuario.id_usuario"), nullable=False)

   
    carritoF = relationship("Carrito", back_populates="facturaC")
    usuarioF = relationship("Usuario", back_populates="facturaU")
    

    
    def __repr__(self):
        return (f'Factura {self.id_factura}\n'
                f'Cliente: {self.usuarioF.id_usuario}\n'
                f'Carrito: {self.carritoF.id_carrito}\n'
                f'Metodo de pago: {self.metodo_pago}\n'
                f'Subtotal: {self.subtotal}\n'
                f'Total: {self.total}\n'
                f'Descuento aplicado: {self.descuento}'
                )
    
    def to_dict(self):
        return {'ID Factura': str(self.id_factura),
                'Cliente': {
                    'ID cliente':str(self.carritoF.id_usuario),
                    'Nombre Completo': f"{self.usuarioF.primer_nombre} {self.usuarioF.segundo_nombre or ''} "
                                         f"{self.usuarioF.primer_apellido} {self.usuarioF.segundo_apellido or ''}"
                    },
                'Carrito': {
                    'ID Carrito':{self.carritoF.id_carrito},
                    'Productos':[
                    {
                    'ID producto': str(dc.producto.id_producto),
                    'Nombre': dc.producto.nombre_producto,
                    'Precio': dc.producto.precio_producto
                    }for dc in self.carritoF.productos
                ],
                'Metodo de pago': self.metodo_pago,
                'Subtotal': self.subtotal,
                'Total': self.total,
                'Descuento': self.descuento
                }
                }
        

class FacturaBase(BaseModel):
   
    metodo_pago: str = Field(..., min_lenght=4,max_lenght=20, description="Que metodo de pago utilizo el cliente.")
    subtotal: Optional[Float] = Field(None, description="")
    total: Float = Field(..., description="Es el total de pago por todos los productos.")
    descuento: Float = Field(None, description="Cuanto descuento se aplico al total, para reducir el precio total.")
    id_carrito: UUID = Field(..., description="Es para saber el carrito del cliente, y su contenido.")
    id_usuario: UUID = Field(..., description="De quien es la factura.")
    fecha_creacion: datetime = Field(..., description= "Fecha de creación del registro de la factura.")

        


class RespuestaFactura(FacturaBase):
    
    id: int
    metodo_pago = str
    subtotal = Float
    total = Float
    descuento = Float
    id_carrito= ForeignKey
    id_usuario = ForeignKey
    id_usuarioCrea: ForeignKey
    fecha_creacion: datetime
    fecha_actul: Optional[datetime] = None 
    
    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}

class ListaFactura(BaseModel):
    
    factura: List[RespuestaFactura]
    total: int
    pagina: int
    por_pagina: int
    
    class Config:
        from_attributes = True

    

