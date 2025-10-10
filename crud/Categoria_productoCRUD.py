"""
Módelo con las operaciones CRUD de Categorias
"""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from Entidades.Categoria_prod import Categoria


class CategoriaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_categoria(
        self, nombre_categoria: str, descripcion: str = None
    ) -> Categoria:
        """
        Módulo para crear una categoria con validaciones buenas.

        Args:
            nombre_categoria: Nombre de la categoría, la cual sera unica y con maximo de 50 caracteres.
            descripcion: Descripción opcional de la categoria

        Returns:
            Categoría creada

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not nombre_categoria or len(nombre_categoria.strip()) == 0:
            raise ValueError("El nombre de la categoría es obligatorio.")

        if len(nombre_categoria) > 50:
            raise ValueError("El nombre no puede exceder 50 caracteres.")

        if self.obtener_categoria_por_nombre(nombre_categoria):
            raise ValueError("Ya existe una categoría con ese nombre")

        categoria = Categoria(
            nombre_categoria=nombre_categoria.strip(),
            descripcion=descripcion.strip() if descripcion else None,
        )
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def obtener_categoria(self, id_categoria: UUID) -> Optional[Categoria]:
        """
        Módulo para buscar y mostrar una categoria por su nombre

        Args:
            id_categoria: UUID de la categoría

        Returns:
            Categoría encontrada o None
        """
        return (
            self.db.query(Categoria)
            .filter(Categoria.id_categoria == id_categoria)
            .first()
        )

    def obtener_categoria_por_nombre(
        self, nombre_categoria: str
    ) -> Optional[Categoria]:
        """
        Módulo para obtener una categoría por nombre

        Args:
            nombre_categoria: Nombre de la categoría

        Returns:
            Categoría encontrada o None
        """
        return (
            self.db.query(Categoria)
            .filter(Categoria.nombre_categoria == nombre_categoria.strip())
            .first()
        )

    def obtener_categorias(self, skip: int = 0, limit: int = 100) -> List[Categoria]:
        """
        Módulo para obtener una lista de categorías con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de categorías
        """
        return self.db.query(Categoria).offset(skip).limit(limit).all()

    def actualizar_categoria(self, id_categoria: UUID, **kwargs) -> Optional[Categoria]:
        """
        Módulo para actualizar una categoría buena (validaciones).

        Args:
            id_categoria: UUID de la categoría
            **kwargs: Campos a actualizar

        Returns:
            Categoría actualizada o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        categoria = self.obtener_categoria(id_categoria)
        if not categoria:
            return None

        if "nombre_categoria" in kwargs:
            nombre = kwargs.pop("nombre_categoria")
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre de la categoría es obligatorio.")
            if len(nombre) > 50:
                raise ValueError("El nombre no puede exceder 50 caracteres.")
            if (
                self.obtener_categoria_por_nombre(nombre)
                and self.obtener_categoria_por_nombre(nombre).id != id_categoria
            ):
                raise ValueError("Ya existe una categoría con ese nombre.")
            kwargs["nombre"] = nombre.strip()

        if "descripcion" in kwargs and kwargs["descripcion"]:
            kwargs["descripcion"] = kwargs["descripcion"].strip()

        if id_usuarioActual is None:
            from Entidades.Usuario import Usuario

            admin = (
                self.db.query(Usuario)
                .filter(Usuario.rol == ("administrador").lower())
                .first()
            )
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar la categoría"
                )
            id_usuarioActual = admin.id_usuario

        categoria.id_usuarioActual = id_usuarioActual

        for key, value in kwargs.items():
            if hasattr(categoria, key):
                setattr(categoria, key, value)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria
