from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional, List
from ..database.database import Base
from uuid import UUID, uuid4
class Proveedor(Base):
    """
     Modelo de un Proveedor, la cual sera una tabla.
    
        id_proveedor: identificador unico.
        primer_nombre: El primer nombre del proveedor.
        segundo_nombre: El aegundo nombre del proveedor.
        segundo_apellido: El segundo apellido del proveedor.
        segundo_apellido: El segundo apellido del proveedor.
        telefono: Como contactar al proveedor.
        correo: direccion de correo del proveedor.
        id_usuarioCrea: El id del usuario que creo al proveedor. (Auditoria).
        id_usuarioActul: El id del usuario que actualizo al proveedor. (Auditoria).
        fecha_creacion: La fecha de creación del proveedor. (Auditoria).
        fecha_actualizacion: la fecha de actualizacion del proveedor. (Auditoria).
    """

    __tablename__= 'Proveedor'

    id_proveedor = Column(UUID(as_uuid=True), primary_key=True, default=UUID.uuid4() ,nullable=False)
    primer_nombre = Column(String(50), nullable=False)
    segundo_nombre = Column(String(50), nullable=True)
    primer_apellido = Column(String(50), nullable=False)
    segundo_apellido = Column(String(50), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=False)
    id_usuarioCrea = Column(UUID, ForeignKey("Usuario.id_usuario"), nullable=False)
    id_usuarioActual = Column(UUID, ForeignKey("Usuario.id_usuario"), nullable=True)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.now)
    fecha_actualizacion = Column(DateTime, nullable=True)
    
    usuarioCreador = relationship("Usuario", back_populates="proveedorCreado")
    usuarioActualizador = relationship("Usuario", back_populates= "proveedorActualizado")
    
    

    def __repr__(self):
        return f"<Proveedor: {self.id_proveedor}\nNombre completo: '{self.primer_nombre," ", self.segundo_nombre, " ", self.primer_apellido," ",self.segundo_apellido}.\nCorreo: {self.correo}'\nTelefono: {self.telefono}.>"
    
    def to_dict(self):
        return {'ID': self.id_proveedor,
                'Primer nombre': self.primer_nombre,
                'Segundo nombre': self.segundo_nombre,
                'Primer apellido': self.primer_apellido,
                'Segundo apellido': self.segundo_apellido,
                'Correo': self.correo,
                'Telefono': self.telefono
                }
    
class ProveedorBase(BaseModel):
    primer_nombre: str = Field(..., min_length=3, max_length=15, description= "Primer nombre del proveedor")
    segundo_nombre: Optional[str] = Field(None, min_length=3, max_length=15, description= "segundo nombre del proveedor")
    primer_apellido: str = Field(..., min_length=3, max_length=15, description= "Primer apellido del proveedor")
    segundo_apellido: Optional[str] = Field(None, min_length=3, max_length=15, description= "segundo apellido del proveedor")
    correo: EmailStr = Field(..., min_length=5, max_length=150, description= "Correo electronico del proveedor")
    telefono: Optional[str] = Field(None, min_length=4, max_length=20, description= "Número de contacto del proveedor")
    id_usuarioCrea: UUID = Field(..., description= "ID del usuario que creo el registro del proveedor.")
    id_usuarioActual: Optional[UUID] = Field(None, description="ID del usuario que actualizo el registro del proveedor.")
    fecha_creacion: datetime = Field(..., description= "Fecha de creación del registro del proveedor.")
    fecha_actualizacion: Optional[datetime] = Field(None, description="Fecha de actualización del registro del proveedor.")
   
    
    @field_validator('primer_nombre')
    def val_primerNombre(cls, v):
        if not v.strip():
            raise ValueError('Lo siento, el primer nombre no puede estar vacío.')
        return v.strip().title()
        
    @field_validator('primer_apellido')
    def val_primerapellido(cls, v):
        if not v.strip():
            raise ValueError('Lo siento, el primer apellido no puede estar vacío.')
        return v.strip().title()

    @field_validator('correo')
    def val_correo(cls, v):
        if not v.strip():
            raise ValueError('El correo no puede quedar vacío.')
        return v.strip().title()
    
    @field_validator('telefono')
    def valTel(cls, v):
        if v is not None:
            v = v.strip()
            if v and not v.replace('+','').replace('-','').replace(' ','').replace('(','').replace(')','').isdigit():
                raise ValueError('Formato de telefono no apto.')
        return v


class CrearProveedor(ProveedorBase):
    """Clase para crear un Proveedor"""
    
    if (self.Usuario.rol == 'administrador'):
        primer_nombre:str = Field(..., min_length=3, max_length=15)
        segundo_nombre: Optional[str] = Field(None, min_length=3, max_length=15)
        primer_apellido: str = Field(..., min_length=3, max_length=15)
        segundo_apellido: Optional[str] = Field(None, min_length=3, max_length=15)
        correo: EmailStr = ...
        telefono: Optional[str] = Field(None, max_length=20)
        activo: Optional[bool] = Field(True)
        id_usuarioCrea: UUID = Field(...)
        fecha_creacion: datetime = Field(...)
    
        @field_validator('primer_nombre')
        def val_primerNombre(cls, v):
            if v is not None and not v.strip():
                raise ValueError('Lo siento, el primer nombre no puede estar vacío.')
            return v.strip().title() if v else v
        
        @field_validator('primer_apellido')
        def val_primerapellido(cls, v):
            if v is not None and not v.strip():
             raise ValueError('Lo siento, el primer apellido no puede estar vacío.')
            return v.strip().title() if v else v
    
        @field_validator('correo')
        def val_correo(cls, v):
            if not v.strip():
                raise ValueError('El correo no puede quedar vacío.')
            return v.strip().title()
    
    
        @field_validator('telefono')
        def valTel(cls, v):
            if v is not None:
                v = v.strip()
                if v and not v.replace('+','').replace('-','').replace(' ','').replace('(','').replace(')','').isdigit():
                    raise ValueError('Formato de telefono no apto.')
            return v
    else:
        print("Lo siento, pero usted no es un administrador, por lo tanto no puede actualizar los registros.")
    




class ActualizarProveedor(ProveedorBase):
    """Clase para actualizar algo de un Proveedor existente"""
    
    if(self.Usuario.rol == 'administrador'):
        
        primer_nombre: Optional[str] = Field(None, min_length=3, max_length=15)
        segundo_nombre: Optional[str] = Field(None, min_length=3, max_length=15)
        primer_apellido: Optional[str] = Field(None, min_length=3, max_length=15)
        segundo_apellido: Optional[str] = Field(None, min_length=3, max_length=15)
        correo: Optional[EmailStr] = None
        telefono: Optional[str] = Field(None, max_length=20)
        activo: Optional[bool] = Field(True)
        id_usuarioActual: UUID = Field(...)
        fecha_actualizacion: DateTime = Field(...)
    
        @field_validator('primer_nombre')
        def val_primerNombre(cls, v):
            if v is not None and not v.strip():
                raise ValueError('Lo siento, el primer nombre no puede estar vacío.')
            return v.strip().title() if v else v
        
        @field_validator('primer_apellido')
        def val_primerapellido(cls, v):
            if v is not None and not v.strip():
             raise ValueError('Lo siento, el primer apellido no puede estar vacío.')
            return v.strip().title() if v else v
    
        @field_validator('correo')
        def val_correo(cls, v):
            if not v.strip():
                raise ValueError('El correo no puede quedar vacío.')
            return v.strip().title()
    
    
        @field_validator('telefono')
        def valTel(cls, v):
            if v is not None:
                v = v.strip()
                if v and not v.replace('+','').replace('-','').replace(' ','').replace('(','').replace(')','').isdigit():
                    raise ValueError('Formato de telefono no apto.')
            return v

    else:
        print("Lo siento, pero usted no es un administrador, por lo tanto no puede actualizar los registros.")
class RespuestaProveedor(ProveedorBase):
    
    id: int
    fecha_creacion: datetime
    fecha_actulizacion: Optional[datetime] = None 
    
    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class ListaProveedores(BaseModel):
    
    usuarios: List[RespuestaProveedor]
    total: int
    pagina: int
    por_pagina: int
    
    class Config:
        from_attributes = True

