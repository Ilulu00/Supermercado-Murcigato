"""
API de carrito. Endpoint para la gestion de los carritos.
"""

from typing import List
from uuid import UUID

from crud.CarritoCRUD import CarritoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import CrearCarrito, RespuestaCarrito, CarritoOut, CarritoListResponse
from sqlalchemy.orm import Session, joinedload
from Entidades.Carrito import Carrito
from Entidades.Detalle_carrito import Detalle_carrito

router = APIRouter(prefix="/carritos", tags=["Carrito"])


@router.post("/", response_model=RespuestaCarrito)
def crear_carrito_de_compras(carrito: CrearCarrito, db: Session = Depends(get_db)):
    """
    Módulo para crear un carrito, en este caso vacio. El carrito se llena es en detalle_carrito

    """
    carrito_crud = CarritoCRUD(db)
    try:
        nuevo_carrito = carrito_crud.crear_carrito(
            id_usuario=carrito.id_usuario, activo=True
        )
        return nuevo_carrito

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear carrito: {str(e)}")


@router.get("/{id_carrito}", response_model=CarritoOut)
def ver_carrito(id_carrito: UUID, db: Session = Depends(get_db)):
    """
    Módulo API para ver el carrito
    """
    try:
        carrito_crud = CarritoCRUD(db)
        carrito_usuario = carrito_crud.ver_carrito(id_carrito)
        return carrito_usuario 
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontro el carrito, error: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al buscar el carrito: {str(e)}",
        )


@router.get("/", response_model=CarritoListResponse)
def listar_carritos(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    """
    Módulo para listar todos los carritos que existan

    """
    try:
        carrito_crud = CarritoCRUD(db)

        total_items = carrito_crud.contar_carritos()
        total_pages = (total_items + size - 1) // size

        if page < 1:
            page = 1

        skip = (page - 1) * size
        carritos = carrito_crud.listar_carritos(skip=skip, limit=size)

        carritos_data = [CarritoOut.model_validate(cr) for cr in carritos]
        return CarritoListResponse(
            data=carritos_data,
            totalPages=total_pages,
            currentPage=page,
            totalItems=total_items,
            size=size,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los carritos: {str(e)}",
        )
