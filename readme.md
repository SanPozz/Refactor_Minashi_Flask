# Minashi - Gestión de Minerales

Minashi es una aplicación web para la gestión, venta y administración de minerales. Permite a usuarios comprar minerales, gestionar pedidos, visualizar el stock, administrar usuarios y exportar datos en CSV. El proyecto está desarrollado con Flask, SQLAlchemy y Tailwind CSS.

## Características

- Panel de administración con gestión de minerales, usuarios y pedidos.
- Visualización y búsqueda de stock de minerales.
- Carrito de compras y resumen de pedido.
- Exportación de tablas a CSV.
- Autenticación de usuarios (registro, login, logout).
- Navbar responsivo con iconos y avatar de usuario.
- Integración con API externa para precios de minerales.
- Estilos modernos y responsivos con Tailwind CSS.

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/SanPozz/Refactor_Minashi_Flask.git
   ```

2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno en un archivo `.env`:
   ```
   API_KEY=tu_api_key
   URL_API=https://api.tuapi.com/endpoint
   ```

4. Inicializa la base de datos:
   ```sh
   flask db upgrade
   ```

5. Ejecuta la aplicación:
   ```sh
   flask run
   ```

## Estructura del proyecto

```
minashi/
│
├── templates/           # Archivos HTML (Jinja2)
├── static/              # Archivos estáticos (CSS, JS, imágenes)
├── models/              # Modelos de base de datos
├── routes/              # Blueprints y rutas Flask
├── instance/            # Configuración y archivos de datos
├── .env                 # Variables de entorno
├── .gitignore           # Archivos ignorados por git
├── requirements.txt     # Dependencias Python
└── README.md            # Este archivo
```

## Uso

- Accede a la web y navega por el panel de administración, carrito, stock y pedidos.
- Exporta datos en CSV desde las tablas.
- Administra usuarios y minerales desde el dashboard.


## Autores

Desarrollado por Santiago Pozzolo, Axel Quesada y Sebastian Onacht.