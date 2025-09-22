"""Operaciones CRUD para factura."""

from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from Entidades.Factura import Factura
from Entidades.Detalle_carrito import Detalle_carrito
from Entidades.Usuario import Usuario
from Entidades.Carrito import Carrito
from datetime import datetime

class FacturaCRUD:
    
    def __init__(self, db: Session):
        self.db= db
    
    def crear_factura(
        self,
        id_carrito: UUID,
        id_usuario: UUID,
        lista_detalles: List[Detalle_carrito],
        metodo_pago: str,
        descuento: float  
    ) -> Factura:
        """Módelo para crear una factura.

        Args:
            id_usuario (UUID): A quien pertence la factura.
            id_carrito (UUID): Es el carrito que lleva la relación del cliente y el detalle.
            lista_detalle (Lista): Es el listado de los detalles de los productos.
            metodo_pago (str): El metodo por el cual, el cliente pago.
            descuento (float): El descuento aplicado, segun las reglas del supermercado.
            
        Returns:
            Factura: Devuelve la factura con todo y detalles.
        """
        usuario= self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            raise ValueError('El cliente no existe.')
        
        carrito= self.db.query(Carrito).filter(Carrito.id_carrito == id_carrito).first()
        if not carrito:
            raise ValueError('El carrito no existe, o no se encontro.')
        
        subtotal = sum(detalle.subtotal for detalle in lista_detalles)
        total = subtotal - descuento
        
        factura = Factura(
            id_usuario= id_usuario,
            id_carrito= id_carrito,
            metodo_pago= metodo_pago,
            subtotal= subtotal,
            descuento=descuento,
            total=total,
            fecha_creacion= datetime.now()
        )
        self.db.add(factura)
        self.db.flush()
        
        for detalle in lista_detalles:
            detalle.id_factura = factura.id_factura
            self.db.add(detalle)
        
        self.db.commit()
        self.db.refresh(factura)
        return factura
    
    def ver_factura(self, id_factura: UUID) -> Optional[Factura]:
        """Módulo para ver la factura.

        Args:
            id_factura (UUID): El UUID de la factura a buscar

        Returns:
            Optional[Factura]: Devuelve y muestra la factura si se encontro.
        """
        factura= self.db.query(Factura).filter(Factura.id_factura == id_factura).first()
        
        if not factura:
            raise ValueError('La factura a buscar no existe.')
        
        detalles = self.db.query(Detalle_carrito).filter(Detalle_carrito.id_Factura == id_factura).all()
        
        return {
            "factura": factura,
            "detalle": detalles
        }