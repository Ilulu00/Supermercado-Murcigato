
# 🛒 Supermercado Murcigato - Sistema de Gestión Avanzado

Sistema de gestión de supermercado desarrollado con **Python**, **SQLAlchemy ORM** y **PostgreSQL** para el examen de Programación de Software.

## 📌 Descripción

El Supermercado Murcigato es un sistema de gestión integral que permite la administración completa de productos, usuarios, facturación y carrito de compras, implementando una arquitectura moderna con ORM, API REST y módulos independientes. En este sistema se incluyen algunos módulos principales como:

## 🧩 Módulos principales

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
- **FastAPI** - Framework para el desarrollo de APIs
- **SQLAlchemy 2.0.23** - ORM avanzado
- **PostgreSQL** - Base de datos (Neon Cloud)
- **Pydantic** - Validación de datos
- **Alembic** - Migraciones de base de datos
- **python-dotenv** - Gestión de variables de entorno
- **Uvicorn** - Servidor ASGI 

## 🏗️ Arquitectura del Sistema

```
├── 📂 apis/                  # Routers de las entidades
│   ├── Usuario.py
│   ├── Producto.py
│   ├── Categoria_prod.py
│   ├── Carrito.py
│   ├── Factura.py
│   ├── Proveedor.py
│   └── Detalle_carrito.py
├── 📂 Entidades/             # Modelos SQLAlchemy
│   ├── Usuario.py
│   ├── Producto.py
│   ├── Categoria_prod.py
│   ├── Carrito.py
│   ├── Factura.py
│   ├── Detalle_carrito.py
│   └── Proveedor.py
├── 📁 crud/                  # Lógica CRUD para las entidades
├── 📁 auth/                  # Sistema de autenticación
├── 📂 database/              # Configuración de la base de datos
│   └── config.py
├── .env                   # Variables de entorno (URL BD, etc.)
├── Requerimientos.txt     # Dependencias del proyecto
├── 👑 main.py             # Punto de entrada del sistema
└── schemas.py             # Esquemas de las entidades
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
<sub> Si depronto ya esta creado el archivo .env, omite este paso.</sub>

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
- **Relaciones complejas** entre entidades
- **UUIDs** como identificadores únicos

## 👩‍💻 Autores

- **Mariana Díaz Restrepo**
- **Santiago Flórez Serna**

**✨ Grupo 12** - Programación de Software

## 📊 Estado del Proyecto

- ✅ Sistema de autenticación implementado
- ✅ CRUD completo para todas las entidades
- ✅ Validaciones con Pydantic
- ✅ Base de datos PostgreSQL configurada
- ✅ Arquitectura modular implementada
- ✅ Sistema de roles funcional
- ✅ Modelo de APIs en Swagger UI
- ✅ APIs hechas con fastAPI

## 🔄 Próximas Mejoras

- [ ] Sistema de notificaciones
- [ ] Reportes y analytics
- [ ] Integración con sistemas de pago

---

**Versión**: 3.0 (Implementacion de fastAPIs)  
**Última actualización**: Octubre 2025


