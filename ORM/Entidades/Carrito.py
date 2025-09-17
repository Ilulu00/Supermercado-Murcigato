"""
Modelo de la entidad Carrito.
Aqui sera donde se creara la entidad carritocon SQLalchemy, asi como algunas validaciones con pydantic
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional, List
from uuid import uuid4, UUID

Base = declarative_base

class Carrito (Base):
    """
    Modelo de un carro de compras, la cual sera una tabla.
    
        id_carrito: identificador unico.
        id_producto: LLave foranea que conecte los productos y sus datos con Carrito
        id_usuario: El id del usuario al q pertenece el carrito de compras
      
    """
    
    __tablename__ = 'Carrito'
    
    id_carrito= Column(UUID(as_uuid=True), primary_key=True, default= UUID.uuid4(), nullable=False)
    id_producto = Column(UUID(as_uuid=True), ForeignKey("Producto.id_producto"), nullable=False)
    id_usuario = Column(UUID(as_uuid=True), ForeignKey("Usuario.id_usuario"), nullable=False)
    
    
    
    
    
    
    def __repr__(self):
        return f"<Carrito de compras de {self.id_carrito}. \nID del cliente: {self.id_usuario}\nNombre completo: '{self.Usuario.primer_nombre," ", self.Usuario.segundo_nombre, " ", self.Usuario.primer_apellido," ",self.Usuario.segundo_apellido}\n Productos: ."
    
    def to_dict(self):
        return {'ID carrito': self.id_carrito,
                'ID cliente': self.Usuario.id_usuario,
                }
    

class CarritoBase(BaseModel):

    
    
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
        
    @field_validator('direccion')
    def val_direccion(cls, v):
        if not v.strip():
            raise ValueError('La direccion no puede quedar vacía.')
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

class UsuarioCreate(UsuarioBase):
    pass

class ActualizarUsuario(UsuarioBase):
    """Clase para actualizar algo de un usuario existente"""
    
    primer_nombre: Optional[str] = Field(None, min_length=3, max_length=15)
    segundo_nombre: Optional[str] = Field(None, min_length=3, max_length=15)
    primer_apellido: Optional[str] = Field(None, min_length=3, max_length=15)
    segundo_apellido: Optional[str] = Field(None, min_length=3, max_length=15)
    direccion: Optional[str] = Field(None, min_length=2, max_length=100)
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = Field(True)
    
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
    
    @field_validator('telefono')
    def valTel(cls, v):
        if v is not None:
            v = v.strip()
            if v and not v.replace('+','').replace('-','').replace(' ','').replace('(','').replace(')','').isdigit():
                raise ValueError('Formato de telefono no apto.')
        return v


class RespuestaUsuario(UsuarioBase):
    
    id: int
    fecha_registro: datetime
    fecha_actul: Optional[datetime] = None 
    
    class Config:
        from_attributes = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class ListaUsuarios(BaseModel):
    
    usuarios: List[RespuestaUsuario]
    total: int
    pagina: int
    por_pagina: int
    
    class Config:
        from_attributes = True
