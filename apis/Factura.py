"""
API de Factura. Endpoints para operaciones en el api.

"""

from typing import List
from uuid import UUID

from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    RespuestaFactura,
    CrearFactura,
    FacturaListResponse,
    DetalleFacturaRespuesta,
)
from sqlalchemy.orm import Session
from Entidades.Carrito import Carrito
from Entidades.Detalle_carrito import Detalle_carrito
from Entidades.Factura import Factura
from crud.FacturaCRUD import FacturaCRUD


router = APIRouter(prefix="/facturas", tags=["Factura"])


@router.post("/{id_carrito}", response_model=RespuestaFactura)
def crear_factura(
    id_carrito: UUID, factura: CrearFactura, db: Session = Depends(get_db)
):
    try:
        carrito = db.query(Carrito).filter(Carrito.id_carrito == id_carrito).first()
        if not carrito:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se encontró el carrito.",
            )
        id_usuario = carrito.id_usuario

        detalles = (
            db.query(Detalle_carrito)
            .filter(Detalle_carrito.id_carrito == id_carrito)
            .all()
        )

        factura_crud = FacturaCRUD(db)
        nueva_factura = factura_crud.crear_factura(
            id_carrito=id_carrito,
            id_usuario=id_usuario,
            lista_detalles=detalles,
            metodo_pago=factura.metodo_pago,
            descuento=0.0,
        )

        detalles_respuesta: List[DetalleFacturaRespuesta] = [
            DetalleFacturaRespuesta(
                nombre_producto=d.producto.nombre_producto,
                cantidad=d.cantidad,
                precio_producto=d.producto.precio_producto,
                subtotal=d.subtotal,
            )
            for d in detalles
        ]

        return RespuestaFactura(
            id_factura=nueva_factura.id_factura,
            id_usuario=nueva_factura.id_usuario,
            id_carrito=nueva_factura.id_carrito,
            activo=nueva_factura.activo,
            metodo_pago=nueva_factura.metodo_pago,
            subtotal_total=nueva_factura.subtotal_total,
            descuento=nueva_factura.descuento,
            total=nueva_factura.total,
            fecha_creacion=nueva_factura.fecha_creacion,
            detalles=detalles_respuesta,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear la factura: {str(e)}"
        )


@router.get("/ver/{id_factura}", response_model=RespuestaFactura)
def ver_factura(id_factura: UUID, db: Session = Depends(get_db)):
    """
    Módulo API para ver la factura

    """
    try:
        factura_crud = FacturaCRUD(db)
        factura_usuario = factura_crud.ver_factura(id_factura)
        return factura_usuario
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del sistema como: {str(e)}",
        )


@router.get("/", response_model=FacturaListResponse)
def listar_facturas(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    """
    Módulo para listar y mostrar todas las facturas que existan

    """
    try:
        factura_crud = FacturaCRUD(db)

        total_items = factura_crud.contar_facturas()
        total_pages = (total_items + size - 1) // size

        if page < 1:
            page = 1

        skip = (page - 1) * size
        facturas = factura_crud.listar_facturas(skip=skip, limit=size)

        facturas_data = [RespuestaFactura.model_validate(fa) for fa in facturas]
        return FacturaListResponse(
            data=facturas_data,
            totalPages=total_pages,
            currentPage=page,
            totalItems=total_items,
            size=size,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las facturas: {str(e)}",
        )


#
@router.patch("/desactivar/{id_factura}", response_model=RespuestaFactura)
def desactivar_factura(id_factura: UUID, db: Session = Depends(get_db)):
    """
    Módulo para desactivar una factura.

    """
    try:
        factura_crud = FacturaCRUD(db)
        factura = factura_crud.eliminar_factura(id_factura)

        return factura

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Error al buscar la factura, no se encontro. Error: {str(e)}",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error del sistema como: {str(e)}",
        )
