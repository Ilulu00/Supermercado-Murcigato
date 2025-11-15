"""
API de Usuarios - Endpoints para gestión de usuarios
"""

from typing import List
from uuid import UUID

from crud.UsuarioCRUD import UsuarioCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
    UsuarioListResponse,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("/", response_model=UsuarioListResponse)
async def obtener_usuarios(
    page: int = 1, size: int = 10, db: Session = Depends(get_db)
):
    """Obtener todos los usuarios con paginación."""
    try:
        usuario_crud = UsuarioCRUD(db)

        total_items = usuario_crud.contar_usuarios()
        total_pages = (total_items + size - 1) // size

        if page < 1:
            page = 1

        skip = (page - 1) * size
        usuarios = usuario_crud.obtener_usuarios(skip=skip, limit=size)

        usuarios_data = [UsuarioResponse.model_validate(u) for u in usuarios]
        return UsuarioListResponse(
            data=usuarios_data,
            totalPages=total_pages,
            currentPage=page,
            totalItems=total_items,
            size=size,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuarios: {str(e)}",
        )


@router.get("/{id_usuario}", response_model=UsuarioResponse)
async def obtener_usuario(id_usuario: UUID, db: Session = Depends(get_db)):
    """Obtener un usuario por ID."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario(id_usuario)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.get("/correo/{correo}", response_model=UsuarioResponse)
async def obtener_usuario_por_correo(correo: str, db: Session = Depends(get_db)):
    """Obtener un usuario por correo."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.obtener_usuario_por_correo(correo)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener usuario: {str(e)}",
        )


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario."""
    try:
        usuario_crud = UsuarioCRUD(db)
        usuario = usuario_crud.crear_usuario(
            primer_nombre=usuario_data.primer_nombre,
            primer_apellido=usuario_data.primer_apellido,
            correo=usuario_data.correo,
            segundo_nombre=usuario_data.segundo_nombre,
            segundo_apellido=usuario_data.segundo_apellido,
            telefono=usuario_data.telefono,
            es_admin=usuario_data.es_admin,
        )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear usuario: {str(e)}",
        )


@router.put("/{id_usuario}", response_model=UsuarioResponse)
async def actualizar_usuario(
    id_usuario: UUID, usuario_data: UsuarioUpdate, db: Session = Depends(get_db)
):
    """Actualizar un usuario existente."""
    try:
        usuario_crud = UsuarioCRUD(db)

        """ Verificar que el usuario existe """
        usuario_existente = usuario_crud.obtener_usuario(id_usuario)
        if not usuario_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
            )

        """ Filtrar campos None para actualización """
        campos_actualizacion = {
            k: v for k, v in usuario_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return usuario_existente

        usuario_actualizado = usuario_crud.actualizar_usuario(
            id_usuario, **campos_actualizacion
        )
        return usuario_actualizado
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar usuario: {str(e)}",
        )


@router.get("/admin/lista", response_model=List[UsuarioResponse])
async def obtener_usuarios_admin(db: Session = Depends(get_db)):
    """Obtener todos los usuarios administradores."""
    try:
        usuario_crud = UsuarioCRUD(db)
        admins = usuario_crud.obtener_usuarios_admin()
        return admins
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener administradores: {str(e)}",
        )


@router.get("/{usuario_id}/es-admin", response_model=RespuestaAPI)
async def verificar_es_admin(usuario_id: UUID, db: Session = Depends(get_db)):
    """Verificar si un usuario es administrador."""
    try:
        usuario_crud = UsuarioCRUD(db)
        es_admin = usuario_crud.es_admin(usuario_id)
        return RespuestaAPI(
            mensaje=f"El usuario {'es' if es_admin else 'no es'} administrador",
            exito=True,
            datos={"es_admin": es_admin},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al verificar administrador: {str(e)}",
        )
