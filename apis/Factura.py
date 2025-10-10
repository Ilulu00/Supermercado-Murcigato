"""
API de Factura. Endpoints para operaciones en el api.

"""

from typing import List

from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import RespuestaFactura, CrearFactura
from sqlalchemy.orm import Session
import Entidades


router = APIRouter(prefix="/facturas", tags=["Factura"])


@router.post("/", response_model=RespuestaFactura)
def crear_factura(factura: CrearFactura, db: Session = Depends(get_db)):
    """
    Módulo api para crear la factura, la cual se creara con datos ya existentes.

    """
    carrito = (
        db.query(Entidades.Carrito)
        .filter(Entidades.Carrito.id_carrito == factura.id_carrito)
        .first()
    )

    detalles = (
        db.query(Entidades.Detalle_carrito)
        .filter(Entidades.Detalle_carrito.id_carrito == factura.id_carrito)
        .all()
    )

    if not carrito:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro el carrito, por ende no se puede realizar la factura.",
        )

    subtotal = sum(d.subtotal for d in detalles)
    total = subtotal - (factura.descuento or 0)

    nueva_factura = Entidades.Factura(
        id_factura=factura.id_factura,
        metodo_pago=factura.metodo_pago,
        subtotal=subtotal,
        descuento=factura.descuento,
        id_carrito=factura.id_carrito,
        total=total,
    )

    db.add(nueva_factura)
    db.commit()
    db.refresh(nueva_factura)
    return nueva_factura


@router.get("/", response_model=List[RespuestaFactura])
def listar_facturas(db: Session = Depends(get_db)):
    """
    Módulo para listar y mostrar todas las facturas que existan

    """
    facturas = db.query(Entidades.Factura).all()
    if not facturas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron facturas"
        )
    return facturas
