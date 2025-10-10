"""
API de Proveedor - Endpoints para gestión de provedores
"""

from typing import List
from uuid import UUID

from crud.ProveedorCRUD import ProveedorCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ProveedorCreate, ProveedorResponse, ProveedorUpdate
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter(prefix="/proveedor", tags=["proveedor"])


@router.get("/", response_model=List[ProveedorResponse])
async def obtener_proveedores(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Obtener todos los proveedores con paginación."""
    try:
        proveedor_crud = ProveedorCRUD(db)
        proveedor = proveedor_crud.obtener_proveedores(skip=skip, limit=limit)
        return proveedor
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}",
        )


@router.get("/{proveedor_id}", response_model=ProveedorResponse)
async def obtener_proveedor(proveedor_id: UUID, db: Session = Depends(get_db)):
    """Obtener un proveedor por ID."""
    try:
        proveedor_crud = ProveedorCRUD(db)
        proveedor = proveedor_crud.obtener_proveedor(proveedor_id)
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
            )
        return proveedor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener proveedor: {str(e)}",
        )


@router.get("/correo/{correo}", response_model=ProveedorResponse)
async def obtener_proveedor_por_correo(correo: str, db: Session = Depends(get_db)):
    """Obtener un proveedor por correo."""
    try:
        proveedor_crud = ProveedorCRUD(db)
        proveedor = proveedor_crud.obtener_proveedor_por_correo(correo)
        if not proveedor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
            )
        return proveedor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener proveedor: {str(e)}",
        )


@router.post("/", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
async def crear_proveedor(
    proveedor_data: ProveedorCreate, db: Session = Depends(get_db)
):
    """Crear un nuevo proveedor."""
    try:
        proveedor_crud = ProveedorCRUD(db)
        proveedor = proveedor_crud.crear_proveedor(
            primer_nombre=proveedor_data.primer_nombre,
            primer_apellido=proveedor_data.primer_apellido,
            correo=proveedor_data.correo,
            segundo_nombre=proveedor_data.segundo_nombre,
            segundo_apellido=proveedor_data.segundo_apellido,
            telefono=proveedor_data.telefono,
            fecha_creacion= datetime.now()
        )
        return proveedor
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear proveedor: {str(e)}",
        )


@router.put("/{id_proveedor}", response_model=ProveedorResponse)
async def actualizar_proveedor(
    id_proveedor: UUID, proveedor_data: ProveedorUpdate, db: Session = Depends(get_db)
):
    """Actualizar un proveedor existente."""
    try:
        proveedor_crud = ProveedorCRUD(db)

        """ Verificar que el proveedor existe """
        proveedor_existente = proveedor_crud.obtener_proveedor(id_proveedor)
        if not proveedor_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Proveedor no encontrado"
            )

        """ Filtrar campos None para actualización """
        campos_actualizacion = {
            k: v for k, v in proveedor_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return proveedor_existente

        proveedor_actualizado = proveedor_crud.actualizar_proveedor(
            id_proveedor, **campos_actualizacion
        )
        return proveedor_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar proveedor: {str(e)}",
        )
