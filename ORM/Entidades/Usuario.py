"""
Modelo de la entidad Usuario.
Aqui sera donde se creara la entidad usuario con SQLalchemy, asi como algunas validaciones con pydantic
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional, List
from uuid import uuid4, UUID

Base = declarative_base

class Usuario (Base):
    """
    Modelo de un usuario, la cual sera una tabla.
    
        id_usuario: identificador unico.
        primer_nombre: El primer nombre del usuario.
        segundo_nombre: El aegundo nombre del usuario.
        primer_apellido: El primer apellido del usuario.
        segundo_apellido: El segundo apellido del usuario.
        direccion: El lugar de residencia del usuario.
        telefono: Como contactar al usuario.
        correo: direccion de correo del usuario.
        rol: Que papel desempaña el usuario (Cliente/Empleado/Administrador)
        activo: para saber como se encuentra el usuario.
        fecha_registro: Fecha y hora de registro.
        fecha_actul: Fecha y hora de última actualización.
    """
    
    __tablename__ = 'Usuarios'
    
    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default= UUID.uuid4(), nullable=False)
    primer_nombre = Column(String(50), nullable=False)
    segundo_nombre = Column(String(50), nullable=True)
    primer_apellido = Column(String(50), nullable=False)
    segundo_apellido = Column(String(50), nullable=True)
    direccion = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=False)
    rol = Column(String(20), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_registro = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actul = Column(DateTime, default=datetime.now, onupdate=datetime.now )
    
    proveedorCreado = relationship("Proveedor", back_populates= "usuarioCreador")
    proveedorActualizado = relationship("Proveedor", back_populates= " usuarioActualizador")
    
    
    
    
    def __repr__(self):
        return f"<Usuario {self.id_usuario}\nNombre completo: '{self.primer_nombre," ", self.segundo_nombre, " ", self.primer_apellido," ",self.segundo_apellido}.\nDireccion: {self.direccion}.\nCorreo: {self.correo}'\nTelefono: {self.telefono}\n Rol: {self.rol}.>"
    
    def to_dict(self):
        return {'ID': self.id_usuario,
                'Primer nombre': self.primer_nombre,
                'Segundo nombre': self.segundo_nombre,
                'Primer apellido': self.primer_apellido,
                'Segundo apellido': self.segundo_apellido,
                'Direccion': self.direccion,
                'Correo': self.correo,
                'Telefono': self.telefono,
                'Rol': self.rol,
                'activo': self.activo,
                'Fecha de registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
                'Fecha actualizacion': self.fecha_actul.isoformat() if self.fecha_actul else None
                }
    

class UsuarioBase(BaseModel):
    primer_nombre: str = Field(..., min_length=3, max_length=15, description= "Primer nombre del usuario")
    segundo_nombre: Optional[str] = Field(None, min_length=3, max_length=15, description= "segundo nombre del usuario")
    primer_apellido: str = Field(..., min_length=3, max_length=15, description= "Primer apellido del usuario")
    segundo_apellido: Optional[str] = Field(None, min_length=3, max_length=15, description= "segundo apellido del usuario")
    direccion: EmailStr = Field(..., min_length=2, max_length=100, description= "Lugar de residencia del usuario")
    correo: str = Field(..., min_length=5, max_length=150, description= "Correo electronico del usuario")
    telefono: Optional[str] = Field(None, min_length=4, max_length=20, description= "Número de contacto del usuario")
    rol: String = Field(..., min_length=5, max_length=20, description= "Rol que identifica al usuario.")
    activo: bool = Field(True, description= "Señal del usuario, para verificar si esta activo o no")
    
    
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
    
    @field_validator('rol')
    def val_rol(cls, v):
            if not v.script():
                raise ValueError('El rol no puede estar vacio, todos los usuarios tiene un rol')
            return f"Su rol es: {v.strip()}"
            
    
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
    """Clase para crear un usuario"""
    
    primer_nombre: str = Field(..., min_length=3, max_length=15)
    segundo_nombre: Optional[str] = Field(None, min_length=3, max_length=15)
    primer_apellido: str = Field(..., min_length=3, max_length=15)
    segundo_apellido: Optional[str] = Field(None, min_length=3, max_length=15)
    direccion: str = Field(..., min_length=2, max_length=100)
    correo: EmailStr = ...
    telefono: Optional[str] = Field(None, max_length=20)
    rol: String = Field(..., min_length=5, max_length=20)
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
