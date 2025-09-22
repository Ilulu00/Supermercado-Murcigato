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

    __tablename__ = "Categorias"

    id_categoria = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre_categoria = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actul = Column(DateTime, onupdate=datetime.now)

    id_usuarioCrea = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=False
    )
    id_usuarioActual = Column(
        UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True
    )

    productos = relationship("Producto", back_populates="categoria")

    usuarioCrea = relationship(
        "Usuario", foreign_keys=[id_usuarioCrea], overlaps="usuario_edita,productos"
    )
    usuarioActual = relationship(
        "Usuario", foreign_keys=[id_usuarioActual], overlaps="usuario_crea,productos"
    )

    def __repr__(self):
        return f"<Categoria(id_categoria={self.id_categoria}, nombre='{self.nombre}')>"
