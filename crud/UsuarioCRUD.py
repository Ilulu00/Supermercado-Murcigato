"""
Operaciones CRUD para el usuario
"""

import re
from typing import List, Optional
from uuid import UUID

import bcrypt
from sqlalchemy.orm import Session

from Entidades.Usuario import Usuario


class UsuarioCRUD:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def hash_contraseña(contraseña: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(contraseña.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    @staticmethod
    def verificar_contraseña(contraseña: str, hashed: str) -> bool:
        return bcrypt.checkpw(contraseña.encode("utf-8"), hashed.encode("utf-8"))

    def validar_correo(self, correo: str) -> bool:
        """Para validar que el correo este bien"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, correo) is not None

    def validar_telefono(self, telefono: str) -> bool:
        """Para validar que el telefono este bien"""
        pattern = r"^\+?[\d\s\-\(\)]{7,15}$"
        return re.match(pattern, telefono) is not None

    def crear_usuario(
        self,
        primer_nombre: str,
        primer_apellido: str,
        correo: str,
        contraseña: str,
        direccion: str,
        segundo_nombre: str = None,
        segundo_apellido: str = None,
        telefono: str = None,
        rol: str = "Cliente",
        rol_forzado: str = None,
    ) -> Usuario:
        """
        Crear un nuevo usuario con validaciones

        Args:
            primer_nombre: Nombre primero del usuario, maximo de 20 caracteres.
            primer_apellido: apellido del usuario, no puede exceder los 20 caracteres.
            correo: correo válido y único
            contraseña: Contraseña segura
            telefono: Teléfono opcional

        Returns:
            Usuario creado

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

        if self.obtener_usuario_por_correo(correo):
            raise ValueError("El correo ya está registrado")

        if not contraseña:
            raise ValueError("La contraseña es obligatoria")
        else:
            self.hash_contraseña(contraseña)

        if telefono and not self.validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        if not direccion:
            raise ValueError("La direccion es obligatoria")

        contraseña_hash = self.hash_contraseña(contraseña)
        rol_final = rol_forzado if rol_forzado else rol

        usuario = Usuario(
            primer_nombre=primer_nombre.lower().strip(),
            segundo_nombre=segundo_nombre.strip() if segundo_nombre else None,
            primer_apellido=primer_apellido.strip(),
            segundo_apellido=segundo_apellido.strip() if segundo_apellido else None,
            correo=correo.lower().strip(),
            telefono=telefono.strip() if telefono else None,
            direccion=direccion,
            rol=rol_final.lower(),
            contraseña=contraseña_hash,
        )

        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario(self, id_usuario: UUID) -> Optional[Usuario]:
        """Para obtener y/o buscar a un usuario por el id.

        Args: id_usuario: UUID del usuario

        Returns: Si se encontro al usuario, el usuario, o nada (None)
        """
        return self.db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()

    def obtener_usuario_por_correo(self, correo: str) -> Optional[Usuario]:
        """Buscar y mostrar un usuario por el correo.

        Args: correo: correo del usuario, por ende el usuario.

        Returns: Usuario o None, sino lo encontro o no existe
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.correo == correo.lower().strip())
            .first()
        )

    def autenticar_usuario(self, correo: str, contraseña: str) -> Optional[Usuario]:
        """Modulo para autenticar y poder registrar al usuario

        Args:
            correo: correo del usuario que registro.
            contraseña: la contraseña unica del usuario.

        Returns: Usuario encontrado o un None.
        """
        usuario = self.obtener_usuario_por_correo(correo)

        if not usuario or not usuario.activo:
            return None

        if not self.verificar_contraseña(contraseña, usuario.contraseña):
            return None
        else:
            return usuario

    def cambiar_contraseña(
        self, id_usuario: UUID, contraseña_actual: str, nueva_contraseña: str
    ) -> bool:
        """Modulo para cambiar la contraseña del usuario

        Args:
            id_usuario: UUID del usuario que quiere cambiar la contraseña.
            contraseña_actual: guarda la contraseña actual.
            contraseña_nueva: contraseña nueva

        Returns: True si se pudo hacer el cambio, si no se pudo       devuelve False

        Raises:
            ValueError: por si la contraseña nueva es invalida
        """
        usuario = self.obtener_usuario(id_usuario)
        if not usuario:
            return False

        if not self.verificar_contraseña(contraseña_actual, usuario.contraseña):
            return False

        usuario.contraseña = self.hash_contraseña(nueva_contraseña)
        self.db.commit()
        return True

    def obtener_usuarios(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """Modulo para mostrar una lista de usuarios con paginas.

        Args:
            skip: numero de registros a skipear.
            limit: numero de registros a mostrar.

        Returns:
            Lista de usuarios.
        """
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def actualizar_usuario(
        self, id_usuario: UUID, id_usuarioActual, **kwargs
    ) -> Optional[Usuario]:
        """Modulo para actualizar alguna usuario, usando validaciones.

        Args:
            id_usuario: UUID del usuario
            id_usuarioActual: UUID del usuario (admin) que edito al usuario.
            **kwargs: campos a actualizar

        Returns: Usuario actualizado o None

        Raises:
            ValueError: si algun dato no es valido.
        """
        usuario = self.obtener_usuario(id_usuario)
        if not usuario:
            return None

        if "correo" in kwargs:
            correo = kwargs.pop("correo")
            if not self.validar_correo(correo):
                raise ValueError("Correo inválido.")
            if (
                self.obtener_usuario_por_correo(correo)
                and self.obtener_usuario_por_correo(correo).id != id_usuario
            ):
                raise ValueError("El correo ya está registrado.")
            kwargs["correo"] = correo.lower().strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            if not self.validar_telefono(kwargs["telefono"]):
                raise ValueError("Telefono inválido.")
            kwargs["telefono"] = kwargs["telefono"].strip()

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuarios_admin(self) -> List[Usuario]:
        """Módulo para obtener todos los usuarios administradores

        Returns:
            Lista de los usuarios administradores
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.rol == ("administrador").lower())
            .all()
        )

    def es_admin(self, id_usuario: UUID) -> bool:
        """Módulo para verificar si un usuario es administrador

        Args:
            id_usuario: UUID del usuario

        Returns:
            True si es administrador, False en caso contrario
        """
        usuario = self.obtener_usuario(id_usuario)
        return usuario.rol.lower() == "administrador" if usuario else False
