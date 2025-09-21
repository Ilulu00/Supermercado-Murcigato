"""
Operaciones CRUD para el proveedor
"""
import re
from typing import List, Optional
from uuid import UUID
from Entidades.Proveedor import Proveedor
from Entidades.Usuario import Usuario
from sqlalchemy.orm import Session
from datetime import datetime


class ProveedorCRUD:
    def __init__(self, db: Session):
        self.db = db

    def validar_correo(self, correo: str) -> bool:
        """Para validar que el correo este bien"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, correo) is not None

    def validar_telefono(self, telefono: str) -> bool:
        """Para validar que el telefono este bien"""
        pattern = r"^\+?[\d\s\-\(\)]{7,15}$"
        return re.match(pattern, telefono) is not None
    
    def crear_proveedor(
        self,
        primer_nombre: str,
        primer_apellido: str,
        correo: str,        
        id_usuarioCrea: UUID,
        id_usuario_logueado: UUID,
        fecha_creacion: datetime,
        segundo_nombre: str = None,
        segundo_apellido: str = None,
        telefono: str = None,
        
        
            ) -> Proveedor:
        """
        Crear un proveedor con validaciones

            Args:
                primer_nombre: Nombre primero del proveedor, maximo de 20 caracteres.
                primer_apellido: apellido del proveedor, no puede exceder los 20 caracteres.
                correo: Correo válido y único
                telefono: Teléfono opcional
        
            Returns:
                Proveedor creado

            Raises:
                ValueError: Si los datos no son válidos
        """
        if not primer_nombre or len(primer_nombre.strip()) == 0:
            raise ValueError("El primer nombre es obligatorio")

        if len(primer_nombre) > 20:
            raise ValueError("El nombre no puede exceder 20 caracteres")

        if not primer_apellido or len(primer_apellido.strip()) == 0:
            raise ValueError("El primer apellido es obligatorio")
        
        if len(primer_apellido) > 20:
            raise ValueError("El primer apellido no puede exceder 20 caracteres")

        if not correo or not self.validar_correo(correo):
            raise ValueError("Correo inválido")

        if self.obtener_proveedor_por_correo(correo):
            raise ValueError("El correo ya está registrado")

        if telefono and not self.validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")
        
        usuario = self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario_logueado).first()
        if not usuario or usuario.rol.lower() != "administrador":
            raise ValueError("Solo un administrador puede crear proveedores.")
  

        proveedor =Proveedor(
            primer_nombre=primer_nombre.lower().strip(),
            segundo_nombre= segundo_nombre.strip() if segundo_nombre else None,
            primer_apellido=primer_apellido.strip(),
            segundo_apellido=segundo_apellido.strip() if segundo_apellido else None,
            correo=correo.lower().strip(),
            telefono=telefono.strip() if telefono else None,
            id_usuarioCrea= id_usuario_logueado,
        )
        self.db.add(proveedor)
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor
    
    def obtener_proveedor(self, id_proveedor: UUID) -> Optional[Proveedor]:
        """Para obtener y/o buscar a un proveedor por el id.
        
            Args: id_usuario: UUID del usuario
        
            Returns: Si se encontro al usuario, el usuario, o nada (None)
        """
        return(
            self.db.query(Proveedor).filter(Proveedor.id_proveedor == id_proveedor).first()
        ) 
        
    def obtener_proveedor_por_correo(self, correo: str) -> Optional[Proveedor]:
        """Buscar y mostrar un proveedor por el correo.

            Args: 
                correo: correo del proveedor, por ende el proveedor.
            
            Returns: proveedor o None, sino lo encontro o no existe
        """    
        return (
            self.db.query(Proveedor).filter(Proveedor.correo == correo.lower().strip()).first()
        )
        
    
    def obtener_proveedores(self, skip: int = 0, limit: int = 100) -> List[Proveedor]:
        """Modulo para mostrar una lista de proveedores con paginas.

            Args: 
                skip: numero de registros a skipear.
                limit: numero de registros a mostrar.
                
            Returns:
                Lista de proveedores.
        """
        return(
            self.db.query(Proveedor).offset(skip).limit(limit).all()
        )
    
    def actualizar_proveedor(self, id_usuarioActual,id_proveedor: UUID, **kwargs) -> Optional[Proveedor]:
        """Modulo para actualizar algun proveedor, usando validaciones.

            Args:
                id_proveedor: UUID del proveedor
                **kwargs: campos a actualizar
                
            Returns: Proveedor actualizado o None
            
            Raises:
                ValueError: si algun dato no es valido.
        """
        usuario = self.db.query(Usuario).filter(Usuario.id_usuario == id_usuarioActual).first()
        if not usuario or usuario.rol.lower() != "administrador":
            raise ValueError("Solo un administrador puede actualizar proveedores.")
        
        proveedor = self.obtener_proveedor(id_proveedor)
        if not proveedor:
            return None
        
        proveedor.fecha_actualizacion = datetime.now()
        proveedor.id_usuarioActual = id_usuarioActual
        
        if "correo" in kwargs:
            correo = kwargs.pop("correo")
            if not self.validar_correo(correo):
                raise ValueError("Correo inválido.")
            if(
                self.obtener_proveedor_por_correo(correo) 
                and self.obtener_proveedor_por_correo(correo).id_proveedor != id_proveedor 
            ):
                raise ValueError("El correo ya está registrado.")
            proveedor.correo = correo.lower().strip()
        
        if "telefono" in kwargs and kwargs["telefono"]:
            telefono = kwargs.pop("telefono")
            if not self.validar_telefono(telefono):
                raise ValueError("Telefono inválido.")
            proveedor.telefono = telefono.strip()
            
        for key, value in kwargs.items():
            if hasattr(proveedor, key):
                setattr(proveedor, key, value)
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor
