"""
Módulo de operaciones CRUD
==========================

Este módulo contiene todas las operaciones CRUD (Create, Read, Update, Delete)
para las entidades del sistema.
"""
#Se vinculan cuando el crud este listo
from .usuario_crud import UsuarioCRUD
from .categoria_crud import CategoriaCRUD
from .producto_crud import ProductoCRUD

__all__ = ['UsuarioCRUD', 'CategoriaCRUD', 'ProductoCRUD']