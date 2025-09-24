
# 🛒 Supermercado Murcigato - Sistema de Gestión Avanzado

Sistema de gestión de supermercado desarrollado con **Python**, **SQLAlchemy ORM** y **PostgreSQL** para el examen de Programación de Software.

## 📌 Descripción

Sistema completo de gestión de supermercado con arquitectura moderna que incluye:

### 👤 **Usuario (Cliente)**
- Autenticación segura con hash de contraseñas
- Visualización de productos con filtros por categoría
- Gestión de carrito de compras
- Sistema de facturación
- Perfil de usuario con información personal

### 🛠 **Administrador**
- Panel de administración completo
- Gestión de usuarios (CRUD)
- Gestión de categorías de productos
- Gestión de productos e inventario
- Control de stock y precios

## 🚀 Tecnologías Utilizadas

- **Python 3** - Lenguaje principal
- **SQLAlchemy 2.0.23** - ORM avanzado
- **PostgreSQL** - Base de datos (Neon Cloud)
- **Pydantic** - Validación de datos
- **Alembic** - Migraciones de base de datos
- **python-dotenv** - Gestión de variables de entorno

## 🏗️ Arquitectura del Sistema

```
ORM/
├── Entidades/          # Modelos SQLAlchemy
│   ├── Usuario.py      # Gestión de usuarios
│   ├── Producto.py     # Gestión de productos
│   ├── Categoria_prod.py # Categorías
│   ├── Carrito.py      # Carrito de compras
│   ├── Factura.py      # Sistema de facturación
│   └── Proveedor.py    # Gestión de proveedores
├── CRUD/               # Operaciones de base de datos
├── auth/               # Sistema de autenticación
├── database/           # Configuración de BD
└── main.py            # Sistema principal
```

## 🔧 Instalación y Configuración

### 1. **Clonar el repositorio**
```bash
git clone https://github.com/Ilulu00/Supermercado-Murcigato
cd Supermercado-Murcigato
```

### 2. **Instalar dependencias**
```bash
pip install -r Requerimientos.txt
```

### 3. **Configurar variables de entorno**
Crear archivo `.env` en la raíz del proyecto:
```env
DATABASE_URL=postgresql://usuario:password@host:port/database
```

### 4. **Ejecutar el sistema**
```bash
python main.py
```

## 🔑 Características Principales

### **Seguridad**
- Autenticación con hash de contraseñas
- Sistema de roles diferenciados
- Validaciones robustas con Pydantic
- Manejo seguro de sesiones

### **Funcionalidades**
- **Gestión de Usuarios**: CRUD completo con validaciones
- **Gestión de Productos**: Control de inventario y stock
- **Sistema de Categorías**: Organización de productos
- **Carrito de Compras**: Gestión de compras
- **Sistema de Facturación**: Generación de facturas
- **Panel de Administración**: Control total del sistema

### **Base de Datos**
- **PostgreSQL** en la nube (Neon)
- **Migraciones automáticas** con Alembic
- **Relaciones complejas** entre entidades
- **UUIDs** como identificadores únicos

## 👩‍💻 Autores

- **Mariana Díaz Restrepo**
- **Santiago Flórez Serna**

**Grupo 12** - Programación de Software

## 📊 Estado del Proyecto

- ✅ Sistema de autenticación implementado
- ✅ CRUD completo para todas las entidades
- ✅ Validaciones con Pydantic
- ✅ Base de datos PostgreSQL configurada
- ✅ Arquitectura modular implementada
- ✅ Sistema de roles funcional

## 🔄 Próximas Mejoras

- [ ] Interfaz web con FastAPI
- [ ] API REST completa
- [ ] Sistema de notificaciones
- [ ] Reportes y analytics
- [ ] Integración con sistemas de pago

---

**Versión**: 2.0 (Implementación ORM)  
**Última actualización**: Enero 2025


# Supermercado Murcigato
Rama qa, llamada tambien rama de calidad. Aunque en nuestro proyecto no sirva de mucho, no entra en la parte laboral de algun proyecto de software.
- Nuestro grupo esta conformado por: Mariana Diaz Restrepo y Santiago Florez Serna, somos el grupo 12.
- Este proyecto trata de un sistema de supermercado, el cual se llama "Murcigato".

