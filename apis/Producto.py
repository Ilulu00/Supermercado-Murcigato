"""
API de Productos - Endpoints para gestión de productos
"""

from typing import List
from uuid import UUID

from crud.ProductoCRUD import ProductoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    ProductoCreate,
    ProductoResponse,
    ProductoUpdate,
    ProductoListResponse,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=ProductoListResponse)
async def obtener_productos(
    page: int = 1, size: int = 10, db: Session = Depends(get_db)
):
    """Obtener todos los productos con paginación."""
    try:
        producto_crud = ProductoCRUD(db)

        total_items = producto_crud.contar_productos()
        total_pages = (total_items + size - 1) // size

        if page < 1:
            page = 1

        skip = (page - 1) * size
        productos = producto_crud.obtener_productos(skip=skip, limit=size)

        productos_respuesta = []
        for p in productos:
            prod_dict = ProductoResponse.model_validate(p).model_dump()
            if p.categoria:
                prod_dict["categoria"] = {"nombre_categoria": p.categoria.nombre}
            else:
                prod_dict["categoria"] = None
            if p.proveedor:
                prod_dict["proveedor"] = {
                    "nombre": f"{p.proveedor.primer_nombre} {p.proveedor.primer_apellido}"
                }
            else:
                prod_dict["proveedor"] = None

            productos_respuesta.append(ProductoResponse(**prod_dict))
        return ProductoListResponse(
            data=productos_respuesta,
            totalPages=total_pages,
            currentPage=page,
            totalItems=total_items,
            size=size,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos: {str(e)}",
        )


@router.get("/{id_producto}", response_model=ProductoResponse)
async def obtener_producto(id_producto: UUID, db: Session = Depends(get_db)):
    """Obtener un producto por ID."""
    try:
        producto_crud = ProductoCRUD(db)
        producto = producto_crud.obtener_producto(id_producto)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )
        return producto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener producto: {str(e)}",
        )


@router.get("/categoria/{id_categoria}", response_model=List[ProductoResponse])
async def obtener_productos_por_categoria(
    id_categoria: UUID, db: Session = Depends(get_db)
):
    """Obtener productos por categoría."""
    try:
        producto_crud = ProductoCRUD(db)
        productos = producto_crud.obtener_productos_por_categoria(id_categoria)
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos por categoría: {str(e)}",
        )


@router.get("/usuario/{id_usuario}", response_model=List[ProductoResponse])
async def obtener_productos_por_usuario(
    id_usuario: UUID, db: Session = Depends(get_db)
):
    """Obtener productos por usuario."""
    try:
        producto_crud = ProductoCRUD(db)
        productos = producto_crud.obtener_productos_por_usuario(id_usuario)
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener productos por usuario: {str(e)}",
        )


@router.get("/buscar/{nombre_producto}", response_model=List[ProductoResponse])
async def buscar_productos_por_nombre(
    nombre_producto: str, db: Session = Depends(get_db)
):
    """Buscar productos por nombre (búsqueda parcial)."""
    try:
        producto_crud = ProductoCRUD(db)
        productos = producto_crud.buscar_productos_por_nombre(nombre_producto)
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar productos: {str(e)}",
        )


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto_data: ProductoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo producto."""
    try:
        producto_crud = ProductoCRUD(db)
        producto = producto_crud.crear_producto(
            nombre_producto=producto_data.nombre_producto,
            precio_producto=producto_data.precio_producto,
            stock=producto_data.stock,
            id_categoria=producto_data.id_categoria,
            id_proveedor=producto_data.id_proveedor,
        )
        return producto
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}",
        )


@router.put("/{id_producto}", response_model=ProductoResponse)
async def actualizar_producto(
    id_producto: UUID, producto_data: ProductoUpdate, db: Session = Depends(get_db)
):
    """Actualizar un producto existente."""
    try:
        producto_crud = ProductoCRUD(db)

        """ Verificar que el producto existe """
        producto_existente = producto_crud.obtener_producto(id_producto)
        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        """ Filtrar campos None para actualización """
        campos_actualizacion = {
            k: v for k, v in producto_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return producto_existente

        producto_actualizado = producto_crud.actualizar_producto(
            id_producto, **campos_actualizacion
        )
        return producto_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar producto: {str(e)}",
        )


@router.patch("/{id_producto}/stock", response_model=ProductoResponse)
async def actualizar_stock(
    id_producto: UUID, nuevo_stock: int, db: Session = Depends(get_db)
):
    """Actualizar el stock de un producto."""
    try:
        producto_crud = ProductoCRUD(db)

        """ Verificar que el producto existe """
        producto_existente = producto_crud.obtener_producto(id_producto)
        if not producto_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado"
            )

        if nuevo_stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El stock no puede ser negativo",
            )

        producto_actualizado = producto_crud.actualizar_stock(id_producto, nuevo_stock)
        return producto_actualizado
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar stock: {str(e)}",
        )
