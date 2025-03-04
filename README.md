# Colecciones Backend

Sistema backend para la gestión de colecciones desarrollado con Django y Django REST Framework.

## Descripción

Este proyecto proporciona una API REST para gestionar colecciones de elementos, permitiendo a los usuarios crear, leer, actualizar y eliminar colecciones y sus elementos asociados.

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Gestor de base de datos (SQLite por defecto)

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd colecciones_backend
   ```

2. **Crear y activar entorno virtual**
   ```bash
   # Crear entorno virtual
   python -m venv venv

   # Activar entorno virtual
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   - Crear archivo `.env` en la raíz del proyecto
   - Copiar contenido de `.env.example` y ajustar valores
   ```
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Aplicar migraciones**
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Iniciar servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

## Uso de la API

### Endpoints Principales

- **Admin Panel**: `/admin/`
- **API Root**: `/api/`
- **Colecciones**: `/api/colecciones/`
- **Elementos**: `/api/elementos/`

### Autenticación

La API utiliza autenticación basada en tokens. Para obtener un token:

1. Crear un usuario en `/admin/`
2. Usar las credenciales para autenticarse
3. Incluir el token en el header de las peticiones:
   ```
   Authorization: Token <tu-token>
   ```

## Desarrollo

### Estructura del Proyecto 