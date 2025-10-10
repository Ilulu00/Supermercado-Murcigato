"""
Operaciones CRUD para Producto
"""

from typing import List, Optional
from uuid import UUID
from Entidades.Proveedor import Proveedor
from Entidades.Producto import Producto
from sqlalchemy.orm import Session


class ProductoCRUD:

    def __init__(self, db: Session):
        self.db = db

    def crear_producto(
        self,
        nombre_producto: str,
        precio_producto: float,
        stock: int,
        id_categoria: UUID,
        id_proveedor: UUID,
    ) -> Producto:
        """
        Crear un nuevo producto con validaciones

        Args:
            nombre_producto: Nombre del producto, el cual no puede ser de mas de 100 caracteres.
            precio_producto: Precio del producto, no puede ser negativo.
            stock: Cantidad en stock, no puede ser negativo al igual que el precio.
            id_proveedor: El UUID del proveedor que proveio el producto
            id_categoria: UUID de la categoría

        Returns:
            Producto creado

        Raises:
            ValueError: Si los datos no son válidos
        """
        if not nombre_producto or len(nombre_producto.strip()) == 0:
            raise ValueError("El nombre del producto es obligatorio.")

        if len(nombre_producto) > 100:
            raise ValueError("El nombre no puede ser mayor a 100 caracteres.")

        if precio_producto <= 0:
            raise ValueError("El precio debe ser mayor a 0.")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

        from Entidades.Categoria_prod import Categoria

        categoria = (
            self.db.query(Categoria)
            .filter(Categoria.id_categoria == id_categoria)
            .first()
        )
        if not categoria:
            raise ValueError("La categoría especificada no existe.")

        proveedor = (
            self.db.query(Proveedor)
            .filter(Proveedor.id_proveedor == id_proveedor)
            .first()
        )
        if not proveedor:
            raise ValueError("El proveedor especificado no existe.")

        producto = Producto(
            nombre_producto=nombre_producto.strip(),
            precio_producto=precio_producto,
            stock=stock,
            categoria=categoria,
            proveedor=proveedor,
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener_producto(self, id_producto: UUID) -> Optional[Producto]:
        """
        Obtener un producto por ID

        Args:
            producto_id: UUID del producto

        Returns:
            Producto encontrado o None
        """
        return (
            self.db.query(Producto).filter(Producto.id_producto == id_producto).first()
        )

    def obtener_productos(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        """
        Obtener lista de productos con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de productos
        """
        return self.db.query(Producto).offset(skip).limit(limit).all()

    def obtener_productos_por_categoria(self, id_categoria: UUID) -> List[Producto]:
        """
        Obtener productos por categoría

        Args:
            id_categoria: UUID de la categoría

        Returns:
            Lista de productos de la categoría
        """
        return (
            self.db.query(Producto).filter(Producto.id_categoria == id_categoria).all()
        )

    def obtener_productos_por_usuario(self, id_usuario: UUID) -> List[Producto]:
        """
        Obtener productos por usuario

        Args:
            id_usuario: UUID del usuario

        Returns:
            Lista de productos del usuario
        """
        return self.db.query(Producto).filter(Producto.uid_usuario == id_usuario).all()

    def buscar_productos_por_nombre(self, nombre_producto: str) -> List[Producto]:
        """
        Buscar productos por nombre (búsqueda parcial)

        Args:
            nombre: Texto a buscar en el nombre

        Returns:
            Lista de productos que coinciden
        """
        return (
            self.db.query(Producto)
            .filter(Producto.nombre_producto.contains(nombre_producto))
            .all()
        )

    def actualizar_producto(self, id_producto: UUID, **kwargs) -> Optional[Producto]:
        """
        Actualizar un producto con validaciones

        Args:
            id_producto: UUID del producto
            **kwargs: Campos a actualizar

        Returns:
            Producto actualizado o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        producto = self.obtener_producto(id_producto)
        if not producto:
            return None

        if "nombre_producto" in kwargs:
            nombre = kwargs.pop("nombre_producto")
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre del producto es obligatorio.")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede ser mayor a 100 caracteres.")
            producto.nombre_producto = nombre.strip()

        if "precio_producto" in kwargs:
            precio = kwargs.pop("precio_producto")
            if precio <= 0:
                raise ValueError("El precio debe ser mayor a 0.")

        if "stock" in kwargs:
            cantidad = kwargs["stock"]
            if cantidad < 0:
                raise ValueError("El stock no puede ser negativo")

        if "id_categoria" in kwargs:
            from Entidades.Categoria_prod import Categoria

            categoria = (
                self.db.query(Categoria)
                .filter(Categoria.id_categoria == kwargs["id_categoria"])
                .first()
            )
            if not categoria:
                raise ValueError("La categoría especificada no existe.")

        for key, value in kwargs.items():
            if hasattr(producto, key):
                setattr(producto, key, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def actualizar_stock(
        self, id_producto: UUID, nuevo_stock: int
    ) -> Optional[Producto]:
        """
        Actualizar el stock de un producto

        Args:
            id_producto: UUID del producto
            nuevo_stock: Nueva cantidad en stock

        Returns:
            Producto actualizado o None
        """
        return self.actualizar_producto(id_producto, stock=nuevo_stock)
