"""Operaciones CRUD de carrito."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from Entidades.Carrito import Carrito
from Entidades.Usuario import Usuario
from Entidades.Detalle_carrito import Detalle_carrito
from Entidades.Producto import Producto
from schemas import CarritoOut, DetalleCarritoOut, RespuestaCarrito


class CarritoCRUD:
    def ver_carrito(self, id_carrito: UUID) -> Optional[CarritoOut]:
        """
        Módulo para visualizar el carrito del cliente, con su detalle.

        Args: carrito sirve para mirar si ese carrito existe para poder verlo con todo y detalles, por eso el "detalle".

        Raises: El carro no existe.

        Return: Devuelve y muestra el carrito, con los productos que tenga.
        """
        carrito = (
            self.db.query(Carrito)
            .options(joinedload(Carrito.detalles).joinedload(Detalle_carrito.producto))
            .filter(Carrito.id_carrito == id_carrito)
            .first()
        )
        if not carrito:
            raise ValueError("El carrito no existe. Por ende, no se puede visualizar.")

        detalle_out = [
            DetalleCarritoOut(
                id_detalle=d.id_detalle,
                id_producto=d.id_producto,
                nombre_producto=d.producto.nombre_producto,
                cantidad=d.cantidad,
                precio_producto=d.precio_producto,
                subtotal=d.cantidad * d.precio_producto,
            )
            for d in carrito.detalles
        ]
        return CarritoOut(
            id_carrito=carrito.id_carrito,
            id_usuario=carrito.id_usuario,
            detalles=detalle_out,
            subtotal_general=sum(
                d.cantidad * d.precio_producto for d in carrito.detalles
            ),
            activo=carrito.activo,
            fecha_crea=carrito.fecha_crea,
        )

    def contar_carritos(self):
        return self.db.query(Carrito).count()

    def listar_carritos(self, skip: int = 0, limit: int = 100) -> List[Carrito]:
        """Módulo para mostrar todos los carritos
        Args:
            skip: seran los numeros de registros a skipear.
            limit: el numero limite de registris a mostrar.

        Returns:
            Lista de carritos, y posiblemente tambien los detalles.
        """
        carritos = (
            self.db.query(Carrito)
            .options(joinedload(Carrito.detalles).joinedload(Detalle_carrito.producto))
            .offset(skip)
            .limit(limit)
            .all()
        )

        resultado = []
        for c in carritos:
            subtotal_general = sum(d.cantidad * d.precio_producto for d in c.detalles)
            resultado.append(
                CarritoOut(
                    id_carrito=c.id_carrito,
                    id_usuario=c.id_usuario,
                    fecha_crea=c.fecha_crea,
                    activo=c.activo,
                    detalles=[
                        DetalleCarritoOut(
                            id_detalle=d.id_detalle,
                            id_producto=d.producto.id_producto,
                            nombre_producto=d.producto.nombre_producto,
                            cantidad=d.cantidad,
                            precio_producto=d.precio_producto,
                            subtotal=d.cantidad * d.precio_producto,
                        )
                        for d in c.detalles
                    ],
                    subtotal_general=subtotal_general,
                )
            )
        return resultado

    def __init__(self, db: Session):
        self.db = db

    def crear_carrito(self, id_usuario: UUID, activo: bool = True) -> Carrito:
        """Módulo para crear un carrito vacío de compras.

        Args: id_usuario para saber a que usuario pertence ese carrito.

        Return: Devolvera un carrito vacio, listo para agregarle productos.

        """
        usuario = (
            self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        )
        if not usuario:
            raise ValueError("El usuario especificado no existe.")

        carrito = Carrito(id_usuario=id_usuario, activo=activo)
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

    def actualizar_producto(
        self, id_detalle: UUID, cantidad_nueva: int
    ) -> Optional[Detalle_carrito]:
        """Módulo para actualizar algun producto que este en el carrito."""

        detalle = (
            self.db.query(Detalle_carrito)
            .filter(
                Detalle_carrito.id_detalle == id_detalle,
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

    def eliminar_producto(self, id_detalle: UUID) -> Optional[Detalle_carrito]:
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
                Detalle_carrito.id_detalle == id_detalle,
            )
            .first()
        )

        if not detalle:
            raise ValueError("El producto no existe en el carrito.")

        self.db.delete(detalle)
        self.db.commit()
        return detalle

    def pagar_carrito(self, id_carrito: UUID) -> Carrito:
        """
        Módulo para poder pagar el carrito
        """
        carrito = (
            self.db.query(Carrito)
            .filter(Carrito.id_carrito == id_carrito, Carrito.activo == True)
            .first()
        )
        if not carrito:
            raise ValueError("El carrito a pagar no existe o ya se pago.")

        subtotal_general = sum(det.subtotal for det in carrito.detalles)

        carrito.subtotal_general = subtotal_general

        carrito.activo = False

        self.db.commit()
        self.db.refresh(carrito)
        return carrito
