"""
 Feat--Estrcutra-orm
Entidad Categorias
Módelo de categorias con SQLAlchemy.
"""

from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import UUID, uuid


class Categoria(Base):
    """
    Modelo de Categoria que representa la tabla 'Categorias'

    Atributos:
        id_cateoria: Identificador único del producto
        nombre_categoria: Nombre de la categoria
        descripción: Descripcion de cada categoria
        fecha_creacion: Fecha y hora de creación
        fecha_actualizacion: Fecha y hora de última actualización
        id_usuarioCrea: ID del usuario que creó el producto
        id_usuarioActualiza: ID del usuario que actualizo el producto.
    """

    __tablename__ = "Categorias"

    id_categoria = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre_categoria = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)

    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.now)
    id_usuarioCrea = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuarioActualiza = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    productos = relationship("Producto", back_populates="Categoria")

    usuarioCrea = relationship(
        "Usuario", foreign_keys=[id_usuarioCrea], overlaps="usuario_edita,productos"
    )
    id_usuarioActualiza = relationship(
        "Usuario", foreign_keys=[id_usuarioActualiza], overlaps="usuario_crea,productos"
    )

    def __repr__(self):
        return f"<Categoria(id_categoria={self.id_categoria}, nombre='{self.nombre}')>"

Modelo de Categoría
"""

from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import UUID

class Categoria(Base):
    __tablename__ = "Categoria"
    
    id_categoria = Column(UUID, primary_key=True, index =True, autoincrement=True)
    nombre_categoria = Column(String(50), nullable=False, unique=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    #Campos de auditoría
    id_usuario_crea = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_usuario_edita = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=True)

    #Relación con productos
    producto = relationship("Producto", back_populates="categoria")

    # Relaciones de auditoría
    usuario_crea = relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita")
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea")

    def __repr__(self):
        return f"<Categoria(id_categoria={self.id_categoria}, nombre='{self.nombre}')>"

