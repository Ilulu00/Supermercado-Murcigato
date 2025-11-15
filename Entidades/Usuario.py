"""
Modelo de la entidad Usuario.
Aqui sera donde se creara la entidad usuario con SQLalchemy, asi como algunas validaciones con pydantic
"""

from datetime import datetime
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database.config import Base


class Usuario(Base):
    """
    Modelo de un usuario, la cual sera una tabla.

        id_usuario: identificador unico.
        primer_nombre: El primer nombre del usuario.
        segundo_nombre: El aegundo nombre del usuario.
        primer_apellido: El primer apellido del usuario.
        segundo_apellido: El segundo apellido del usuario.
        telefono: Como contactar al usuario.
        correo: direccion de correo del usuario.
        activo: para saber como se encuentra el usuario.
        fecha_registro: Fecha y hora de registro.
        fecha_actul: Fecha y hora de última actualización.
        es_admin: Dice si el usuario tiene rol de administrador
    """

    __tablename__ = "Usuarios"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False
    )
    primer_nombre = Column(String(50), nullable=False)
    segundo_nombre = Column(String(50), nullable=True)
    primer_apellido = Column(String(50), nullable=False)
    segundo_apellido = Column(String(50), nullable=True)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    es_admin = Column(Boolean, default=False)
    fecha_registro = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actual = Column(DateTime, onupdate=datetime.now)

    usuarioCarrito = relationship("Carrito", back_populates="carritoUsuario")

    facturaU = relationship(
        "Factura", back_populates="usuarioF", foreign_keys="[Factura.id_usuario]"
    )

    def __repr__(self):
        return f"<Usuario {self.id_usuario}\nNombre completo: '{self.primer_nombre} {self.segundo_nombre or ''} {self.primer_apellido} {self.segundo_apellido or ''}'\nDireccion: {self.direccion}\nCorreo: {self.correo}\nTelefono: {self.telefono}>"

    def to_dict(self):
        return {
            "ID": self.id_usuario,
            "Primer nombre": self.primer_nombre,
            "Segundo nombre": self.segundo_nombre,
            "Primer apellido": self.primer_apellido,
            "Segundo apellido": self.segundo_apellido,
            "Correo": self.correo,
            "Telefono": self.telefono,
            "activo": self.activo,
            "Fecha de registro": (
                self.fecha_registro.isoformat() if self.fecha_registro else None
            ),
            "Fecha actualizacion": (
                self.fecha_actual.isoformat() if self.fecha_actual else None
            ),
            "es_admin": self.es_admin,
        }


class UsuarioBase(BaseModel):
    primer_nombre: str = Field(
        ..., min_length=3, max_length=15, description="Primer nombre del usuario"
    )
    segundo_nombre: Optional[str] = Field(
        None, min_length=3, max_length=15, description="segundo nombre del usuario"
    )
    primer_apellido: str = Field(
        ..., min_length=3, max_length=15, description="Primer apellido del usuario"
    )
    segundo_apellido: Optional[str] = Field(
        None, min_length=3, max_length=15, description="segundo apellido del usuario"
    )
    correo: EmailStr = Field(
        ..., min_length=5, max_length=150, description="Correo electronico del usuario"
    )
    telefono: Optional[str] = Field(
        None, min_length=4, max_length=20, description="Número de contacto del usuario"
    )
    activo: bool = Field(
        True, description="Señal del usuario, para verificar si esta activo o no"
    )
    es_admin: bool = Field(
        False, description="Indica si el usuario tiene el rol de administrador"
    )

    @field_validator("primer_nombre")
    def val_primerNombre(cls, v):
        if not v.strip():
            raise ValueError("Lo siento, el primer nombre no puede estar vacío.")
        return v.strip().title()

    @field_validator("primer_apellido")
    def val_primerapellido(cls, v):
        if not v.strip():
            raise ValueError("Lo siento, el primer apellido no puede estar vacío.")
        return v.strip().title()

    @field_validator("correo")
    def val_correo(cls, v):
        if not v.strip():
            raise ValueError("El correo no puede quedar vacío.")
        return v.strip().title()

    @field_validator("telefono")
    def valTel(cls, v):
        if v is not None:
            v = v.strip()
            if (
                v
                and not v.replace("+", "")
                .replace("-", "")
                .replace(" ", "")
                .replace("(", "")
                .replace(")", "")
                .isdigit()
            ):
                raise ValueError("Formato de telefono no apto.")
        return v


class CrearUsuario(UsuarioBase):
    """Clase para crear un usuario"""

    primer_nombre: str = Field(..., min_length=3, max_length=15)
    segundo_nombre: Optional[str] = Field(None, min_length=3, max_length=15)
    primer_apellido: str = Field(..., min_length=3, max_length=15)
    segundo_apellido: Optional[str] = Field(None, min_length=3, max_length=15)
    correo: EmailStr = ...
    telefono: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = Field(True)
    es_admin: bool = Field(False)

    @field_validator("primer_nombre")
    def val_primerNombre(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Lo siento, el primer nombre no puede estar vacío.")
        return v.strip().title() if v else v

    @field_validator("primer_apellido")
    def val_primerapellido(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Lo siento, el primer apellido no puede estar vacío.")
        return v.strip().title() if v else v

    @field_validator("telefono")
    def valTel(cls, v):
        if v is not None:
            v = v.strip()
            if (
                v
                and not v.replace("+", "")
                .replace("-", "")
                .replace(" ", "")
                .replace("(", "")
                .replace(")", "")
                .isdigit()
            ):
                raise ValueError("Formato de telefono no apto.")
        return v


class ActualizarUsuario(UsuarioBase):
    """Clase para actualizar algo de un usuario existente"""

    primer_nombre: Optional[str] = Field(None, min_length=3, max_length=15)
    segundo_nombre: Optional[str] = Field(None, min_length=3, max_length=15)
    primer_apellido: Optional[str] = Field(None, min_length=3, max_length=15)
    segundo_apellido: Optional[str] = Field(None, min_length=3, max_length=15)
    correo: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = Field(True)
    es_admin: Optional[bool] = Field(False)

    @field_validator("primer_nombre")
    def val_primerNombre(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Lo siento, el primer nombre no puede estar vacío.")
        return v.strip().title() if v else v

    @field_validator("primer_apellido")
    def val_primerapellido(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Lo siento, el primer apellido no puede estar vacío.")
        return v.strip().title() if v else v

    @field_validator("telefono")
    def valTel(cls, v):
        if v is not None:
            v = v.strip()
            if (
                v
                and not v.replace("+", "")
                .replace("-", "")
                .replace(" ", "")
                .replace("(", "")
                .replace(")", "")
                .isdigit()
            ):
                raise ValueError("Formato de telefono no apto.")
        return v


from Entidades.Proveedor import Proveedor
from Entidades.Producto import Producto
from Entidades.Carrito import Carrito
from Entidades.Factura import Factura
