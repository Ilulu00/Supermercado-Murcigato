"""
API de carrito. Endpoint para la gestion de los carritos.
"""

from typing import List
from uuid import UUID

from crud.CarritoCRUD import CarritoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import CarritoBase, CrearCarrito, RespuestaCarrito, DetalleCarritoResponse
from sqlalchemy.orm import Session
import Entidades

router = APIRouter(prefix="/carritos", tags=["Carrito"])


@router.post("/", response_model=RespuestaCarrito)
def crear_carrito_de_compras(
    carrito: CrearCarrito, id_usuario: UUID, db: Session = Depends(get_db)
):
    """
    Módulo para crear un carrito, en este caso vacio. El carrito se llena es en detalle_carrito

    """
    carrito_crud = CarritoCRUD(db)
    carrito = carrito_crud.crear_carrito(db, id_usuario=id_usuario)
    db.add(carrito)
    db.commit()
    db.refresh(carrito)
    return carrito


@router.get("/", response_model=list[DetalleCarritoResponse])
def listar_carritos(db: Session = Depends(get_db)):
    """
    Módulo para listar todos los carritos que existan

    """
    detalles = db.query(Entidades.Detalle_carrito).all()
    if not detalles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron detalles de productos.",
        )
    return detalles
