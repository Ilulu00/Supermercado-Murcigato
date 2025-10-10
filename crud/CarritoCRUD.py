"""Operaciones CRUD de carrito."""

from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from Entidades.Carrito import Carrito
from Entidades.Detalle_carrito import Detalle_carrito
from Entidades.Producto import Producto


class CarritoCRUD:

    def __init__(self, db: Session):
        self.db = db

    def crear_carrito(self, id_usuario: UUID) -> Carrito:
        """Módulo para crear un carrito vacío de compras.

        Args: id_usuario para saber a que usuario pertence ese carrito.

        Return: Devolvera un carrito vacio, listo para agregarle productos.

        """

        carrito = Carrito(id_usuario=id_usuario, activo=True)
        self.db.add(carrito)
        self.db.commit()
        self.db.refresh(carrito)
        return carrito

    def agregar_producto(
        self, id_carrito: UUID, id_producto: UUID, cantidad: int
    ) -> Detalle_carrito:
        """Módulo para agregar un producto al carrito.

        Args: carrito sirve para buscar el carrito y asi poder ingresar productos a este.
              producto sirve para serciorarse si ese producto existe o no.

        Raises:
                Si el carro no existe.
                Si ese producto en especifico no existe.

        Return: devolvera el detalle del carrito, con sus productos y demas información.
        """
        carrito = (
            self.db.query(Carrito)
            .filter(Carrito.id_carrito == id_carrito, Carrito.activo == True)
            .first()
        )
        if not carrito:
            raise ValueError("El carrito no existe.")

        producto = (
            self.db.query(Producto).filter(Producto.id_producto == id_producto).first()
        )
        if not producto:
            raise ValueError("El producto seleccionado no existe.")

        subtotal = producto.precio_producto * cantidad

        detalle = Detalle_carrito(
            id_carrito=id_carrito,
            id_producto=id_producto,
            cantidad=cantidad,
            subtotal=subtotal,
        )

        self.db.add(detalle)
        self.db.commit()
        self.db.refresh(detalle)
        return detalle

    def ver_carrito(self, id_carrito: UUID):
        """Módulo para visualizar el carrito del cliente, con su detalle.

        Args: carrito sirve para mirar si ese carrito existe para poder verlo con todo y detalles, por eso el "detalle".

        Raises: El carro no existe.

        Return: Devuelve y muestra el carrito, con los productos que tenga.
        """
        carrito = (
            self.db.query(Carrito).filter(Carrito.id_carrito == id_carrito).first()
        )

        if not carrito:
            raise ValueError("El carrito no existe. Por ende, no se peude visualizar.")

        detalle = (
            self.db.query(Detalle_carrito)
            .filter(Detalle_carrito.id_carrito == id_carrito)
            .all()
        )

        total = sum(det.subtotal for det in detalle)

        return {
            "carrito": carrito,
            "productos": detalle,
            "total": total,
        }

    def actualizar_producto(
        self, id_carrito: UUID, id_producto: UUID, cantidad_nueva: int
    ) -> Optional[Detalle_carrito]:
        """Módulo para actualizar algun producto que este en el carrito."""

        carrito = (
            self.db.query(Carrito).filter(Carrito.id_carrito == id_carrito).first()
        )

        if not carrito:
            raise ValueError("El carrito no existe. No se pueden actualizar productos.")

        detalle = (
            self.db.query(Detalle_carrito)
            .filter(
                Detalle_carrito.id_carrito == id_carrito,
                Detalle_carrito.id_producto == id_producto,
            )
            .first()
        )

        if not detalle:
            raise ValueError("El producto a actualizar no existe en tu carrito.")

        detalle.cantidad = cantidad_nueva
        detalle.subtotal = detalle.producto.precio_producto * cantidad_nueva

        self.db.commit()
        self.db.refresh(detalle)
        return detalle


def eliminar_producto(
    self, id_carrito: UUID, id_producto: UUID
) -> Optional[Detalle_carrito]:
    """
    Módulo para eliminar un producto del carrito

    Raises:
            Si el carrito no existe.
            Si el producto no existe.

    Returns:
        producto_eliminado: Siendo este el producto eliminado.
    """
    detalle = (
        self.db.query(Detalle_carrito)
        .filter(
            Detalle_carrito.id_carrito == id_carrito,
            Detalle_carrito.id_producto == id_producto,
        )
        .first()
    )

    if not detalle:
        raise ValueError("El producto no existe en el carrito.")

    self.db.delete(detalle)
    self.db.commit()
    return detalle
