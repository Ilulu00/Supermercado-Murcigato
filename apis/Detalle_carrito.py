"""
Endpoints de Detalle_carrito. API de Detalle_carrito

"""

from typing import List
from uuid import UUID

from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import DetalleCarritoCreate, DetalleCarritoResponse, DetalleCarritoUpdate
from sqlalchemy.orm import Session
from Entidades.Detalle_carrito import Detalle_carrito
from Entidades.Carrito import Carrito
from Entidades.Producto import Producto

router = APIRouter(prefix="/detalles_carrito", tags=["Detalle_carrito"])


@router.post("/", response_model=DetalleCarritoResponse)
def crear_Detalle_carrito(detalle: DetalleCarritoCreate, db: Session = Depends(get_db)):
    """
    Modulo para crear un detalle, más tirando a una creacion de un producto

    """
    try:

        carrito = (
            db.query(Carrito).filter(Carrito.id_carrito == detalle.id_carrito).first()
        )
        if not carrito:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado."
            )
        producto = (
            db.query(Producto)
            .filter(Producto.id_producto == detalle.id_producto)
            .first()
        )
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado."
            )

        subtotal = producto.precio_producto * detalle.cantidad

        nuevo_detalle = Detalle_carrito(
            id_carrito=detalle.id_carrito,
            id_producto=detalle.id_producto,
            cantidad=detalle.cantidad,
            subtotal=subtotal,
        )

        db.add(nuevo_detalle)
        db.commit()
        db.refresh(nuevo_detalle)
        return nuevo_detalle

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear carrito: {str(e)}")


@router.get("/{id_carrito}", response_model=List[DetalleCarritoResponse])
def buscar_carrito(id_carrito: UUID, db: Session = Depends(get_db)):
    """
    Módulo para mostrar los detalles de un carrito

    """
    detalles = (
        db.query(Detalle_carrito).filter(Detalle_carrito.id_carrito == id_carrito).all()
    )
    if not detalles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El detalle no fue encontrado.",
        )
    return detalles


@router.put("/{id_detalle}", response_model=DetalleCarritoUpdate)
def actualizar_detalle(
    id_detalle: UUID, detalle: DetalleCarritoCreate, db: Session = Depends(get_db)
):
    """
    Módulo para actualizar la cantidad de un producto dentro de un detalle

    """
    db_detalle = (
        db.query(Detalle_carrito) 
        .filter(Detalle_carrito.id_detalle == id_detalle)
        .first()
    )     
    if not db_detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El detalle buscado no fue encontrado.",
        )

    db_detalle.cantidad = detalle.cantidad
    db.commit()
    db.refresh(db_detalle)
    return db_detalle


@router.delete("/{id_detalle}")
def eliminar_producto_detalle(id_detalle: UUID, db: Session = Depends(get_db)):
    detalle = (
        db.query(Detalle_carrito)
        .filter(Detalle_carrito.id_detalle == id_detalle)
        .first()
    )
    if not detalle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El detalle no fue encontrado.",
        )

    db.delete(detalle)
    db.commit()

    return {"mensaje": "Producto eliminado del detalle correctamente."}
