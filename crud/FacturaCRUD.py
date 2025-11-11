"""Operaciones CRUD para factura."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session, joinedload
from Entidades.Factura import Factura
from schemas import DetalleFacturaRespuesta, RespuestaFactura
from Entidades.Detalle_carrito import Detalle_carrito
from Entidades.Usuario import Usuario
from Entidades.Carrito import Carrito
from datetime import datetime


class FacturaCRUD:

    def __init__(self, db: Session):
        self.db = db

    def crear_factura(
        self,
        id_carrito: UUID,
        id_usuario: UUID,
        lista_detalles: List[Detalle_carrito],
        metodo_pago: str,
        descuento: float,
    ) -> Factura:
        """Módelo para crear una factura.

        Args:
            id_usuario (UUID): A quien pertence la factura.
            id_carrito (UUID): Es el carrito que lleva la relación del cliente y el detalle.
            lista_detalle (Lista): Es el listado de los detalles de los productos.
            metodo_pago (str): El metodo por el cual, el cliente pago.
            descuento (float): El descuento aplicado, segun las reglas del supermercado, como que si la compra supera los 50000, se aplicara un descuento del 5%.

        Returns:
            Factura: Devuelve la factura con todo y detalles.
        """
        usuario = (
            self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        )
        if not usuario:
            raise ValueError("El cliente no existe.")

        carrito = (
            self.db.query(Carrito).filter(Carrito.id_carrito == id_carrito).first()
        )
        if not carrito:
            raise ValueError("El carrito no existe, o no se encontro.")

        subtotal = sum(detalle.subtotal for detalle in lista_detalles)

        descuento = 0.0
        if subtotal >= 50000.00:
            descuento = subtotal * 0.05
        elif subtotal >= 100000.00:
            descuento = subtotal * 0.1

        total = subtotal - descuento

        factura = Factura(
            id_usuario=id_usuario,
            id_carrito=id_carrito,
            metodo_pago=metodo_pago,
            subtotal=subtotal,
            descuento=descuento,
            total=total,
            activo=True,
            fecha_creacion=datetime.now(),
        )
        carrito.activo = False

        self.db.add(factura)
        self.db.flush()

        for detalle in lista_detalles:
            detalle.id_factura = factura.id_factura
            self.db.add(detalle)

        self.db.commit()
        self.db.refresh(factura)
        return factura

    def ver_factura(self, id_factura: UUID) -> Optional[RespuestaFactura]:
        """Módulo para ver la factura.
 
        Args:
            id_factura (UUID): El UUID de la factura a buscar

        Returns:
            Optional[Factura]: Devuelve y muestra la factura si se encontro.
        """
        factura = (
            self.db.query(Factura)
            .options(
                joinedload(Factura.carritoF)
                .joinedload(Carrito.detalles)
                .joinedload(Detalle_carrito.producto)
            )
            .filter(Factura.id_factura == id_factura)
            .first()
        )
        if not factura:
            raise ValueError("No existe la factura.")

        detalle_out = [
            DetalleFacturaRespuesta(
                nombre_producto=d.producto.nombre_producto,
                cantidad=d.cantidad,
                precio_producto=d.precio_producto,
                subtotal=d.cantidad * d.precio_producto,
            )
            for d in factura.carritoF.detalles
        ]
        return RespuestaFactura(
            id_factura=factura.id_factura,
            id_usuario=factura.id_usuario,
            id_carrito=factura.id_carrito,
            detalles=detalle_out,
            metodo_pago=factura.metodo_pago,
            subtotal_total=sum(
                d.cantidad * d.precio_producto for d in factura.carritoF.detalles
            ),
            descuento=factura.descuento,
            total=factura.total,
            activo=factura.activo,
            fecha_creacion=factura.fecha_creacion,
        )

    def listar_facturas(self, skip: int = 0, limit: int = 100) -> List[Factura]:
        """
        Módulo para listar y mostrar todas las facturas que existan.

        Args:
            skip: el numero de registros que se quiera skipear.
            limit: limite de registros a mostrar.

        Returns:
            Lista de facturas.
        """
        facturas = (
            self.db.query(Factura)
            .options(
                joinedload(Factura.carritoF)
                .joinedload(Carrito.detalles)
                .joinedload(Detalle_carrito.producto)
            )
            .offset(skip)
            .limit(limit)
            .all()
        )

        resultado = []
        for f in facturas:
            subtotal_total = sum(
                d.cantidad * d.precio_producto for d in f.carritoF.detalles
            )
            resultado.append(
                RespuestaFactura(
                    id_factura=f.id_factura,
                    id_usuario=f.id_usuario,
                    metodo_pago=f.metodo_pago,
                    descuento=f.descuento,
                    total=f.total,
                    activo=f.activo,
                    fecha_creacion=f.fecha_creacion,
                    detalles=[
                        DetalleFacturaRespuesta(
                            nombre_producto=d.producto.nombre_producto,
                            cantidad=d.cantidad,
                            precio_producto=d.precio_producto,
                            subtotal=d.cantidad * d.precio_producto,
                        )
                        for d in f.carritoF.detalles
                    ],
                    subtotal_total=subtotal_total,
                )
            )
        return resultado

    def eliminar_factura(self, id_factura: UUID) -> Factura:
        """
        Módulo para "eliminar" una factura desactivandola.

        Args:
            id_factura: para saber la factura a eliminar

        Returns:
            Factura eliminada.
        """
        factura = (
            self.db.query(Factura).filter(Factura.id_factura == id_factura).first()
        )
        if not factura:
            raise ValueError("La factura a buscar y posterior eliminamiento no existe.")

        factura.activo = False

        self.db.commit()
        self.db.refresh(factura)
        return factura
