"""
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
