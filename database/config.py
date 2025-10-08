"""
Configuración de la base de datos
=================================

Configuraciones centralizadas para la conexión a la base de datos.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""
Cargamos las variables de entorno
"""
load_dotenv()

"""Configuración de la base de datos Neon PostgreSQL
Obtener la URL completa de conexión desde las variables de entorno
"""
DATABASE_URL = os.getenv("DATABASE_URL")

# Si no hay DATABASE_URL, usar la URL de Neon directamente
if not DATABASE_URL:
    DATABASE_URL = "postgresql://neondb_owner:npg_sK9nR5CfYAwB@ep-morning-lake-ad1f3v53-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

"""Crear el motor de SQLAlchemy"""
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "require"},
)

"""Cerrar sesión"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""Base para los modelos en la base de datos"""
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    Base.metadata.create_all(bind=engine)