"""
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