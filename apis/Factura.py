"""
API de Factura. Endpoints para operaciones en el api.

"""

from typing import List

from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import RespuestaFactura, CrearFactura
from sqlalchemy.orm import Session
from Entidades.Carrito import Carrito
from Entidades.Detalle_carrito import Detalle_carrito
from Entidades.Factura import Factura
from crud.FacturaCRUD import FacturaCRUD


router = APIRouter(prefix="/facturas", tags=["Factura"])


@router.post("/", response_model=RespuestaFactura)
def crear_factura(factura: CrearFactura, db: Session = Depends(get_db)):
    """
    Módulo api para crear la factura, la cual se creara con datos ya existentes.

    """
    try:

        carrito = (
            db.query(Carrito).filter(Carrito.id_carrito == factura.id_carrito).first()
        )

        detalles = (
            db.query(Detalle_carrito)
            .filter(Detalle_carrito.id_carrito == factura.id_carrito)
            .all()
        )

        if not carrito:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontro el carrito, por ende no se puede realizar la factura.",
            )

        subtotal = sum(d.subtotal for d in detalles)
        total = subtotal - (factura.descuento or 0)

        nueva_factura = Factura(
            id_usuario=factura.id_usuario,
            id_carrito=factura.id_carrito,
            metodo_pago=factura.metodo_pago,
            subtotal=subtotal,
            descuento=factura.descuento,
            total=total,
            activo=factura.activo,
        )

        db.add(nueva_factura)
        db.commit()
        db.refresh(nueva_factura)
        return nueva_factura

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear la factura: {str(e)}"
        )


@router.get("/", response_model=List[RespuestaFactura])
def listar_facturas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Módulo para listar y mostrar todas las facturas que existan

    """
    try:
        factura_crud = FacturaCRUD(db)
        facturas = factura_crud.listar_facturas(skip=skip, limit=limit)
        return facturas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las facturas: {str(e)}",
        )
