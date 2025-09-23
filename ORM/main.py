"""
Sistema de gestion de productos con ORM SQLAlchemy y Neon PostgreSQL
Incluye sistema de autenticacion con login
"""

import getpass
from typing import Optional

from crud.CarritoCRUD import CarritoCRUD
from crud.Categoria_productoCRUD import CategoriaCRUD
from crud.FacturaCRUD import FacturaCRUD
from crud.ProductoCRUD import ProductoCRUD
from crud.ProveedorCRUD import ProveedorCRUD
from crud.UsuarioCRUD import UsuarioCRUD

from database.config import SessionLocal, create_tables
from Entidades.Carrito import Carrito
from Entidades.Categoria_prod import Categoria
from Entidades.Detalle_carrito import Detalle_carrito
from Entidades.Factura import Factura
from Entidades.Producto import Producto
from Entidades.Proveedor import Proveedor
from Entidades.Usuario import Usuario


class SistemaGestion:
    """Sistema de gestión por consola (menu)"""

    def __init__(self):
        """Inicializar el sistema"""
        self.db = SessionLocal()
        self.carritoCRUD = CarritoCRUD(self.db)
        self.Categoria_productoCRUD = CategoriaCRUD(self.db)
        self.FacturaCRUD = FacturaCRUD(self.db)
        self.ProductoCRUD = ProductoCRUD(self.db)
        self.ProveedorCRUD = ProveedorCRUD(self.db)
        self.UsuarioCRUD = UsuarioCRUD(self.db)
        self.usuario_actual: Optional[Usuario] = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.db.close()

    def login(self) -> bool:
        """Mostrar el Login por consola y autentificar usuario"""
        print("°" * 50)
        print("Bienvenido a Supermercado Murcigato")
        print("Inicio de sesión")

        intentos: int = 0
        max_intentos: int = 4

        while intentos < max_intentos:
            try:
                print(f"\nIntento {intentos + 1} de {max_intentos}")
                nombre_usuario = input("Usuario: ").strip

                if not nombre_usuario:
                    print("El nombre de usuario es obligatorio")
                    intentos += 1
                    continue

                password = getpass.getpass("Contraseña: ")

                if not password:
                    print("La contraseña es obligatoria")
                    intentos += 1
                    continue

                usuario = self.UsuarioCRUD.autenticar_usuario(nombre_usuario, password)

                if usuario:
                    self.usuario_actual = usuario
                    print(f"Bienvenido {usuario.primer_nombre}")
                    if UsuarioCRUD.es_admin:
                        print("Tienes privilegios de administrador")
                    return True
                else:
                    print("Error: información incorecta o perfil inactivo")
                    intentos += 1

            except KeyboardInterrupt:
                print("\nOperación cancelada por el usuario")
                return False

            except Exception as e:
                print(f"Error durante la ejecución: {e}")
                intentos += 1

        print("Se ha llegado al máximo de intentos, acceso denegado")
        return False
