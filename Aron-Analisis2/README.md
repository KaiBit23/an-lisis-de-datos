# Dashboard de Rendimiento Académico

Este proyecto es una aplicación web desarrollada con **Python (Flask)** y **Pandas** para el análisis interactivo de datos académicos universitarios. El diseño utiliza **Tailwind CSS** para una interfaz moderna y profesional.

## Estructura del Proyecto

```text
Aron/
├── data/               # Archivos CSV con la información base
├── src/                # Código fuente de la aplicación
│   ├── templates/      # Archivos HTML (Plantillas de Flask)
│   └── app.py          # Lógica del servidor y procesamiento de datos
├── static/             # Archivos estáticos (CSS, Imágenes)
├── requirements.txt    # Librerías necesarias
└── README.md           # Documentación del proyecto
```

## Requisitos Previos

- Python 3.8 o superior
- Pip (Administrador de paquetes de Python)

## Instalación y Ejecución

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Ejecutar la aplicación**:
   ```bash
   python src/app.py
   ```

3. **Ver resultados**:
   Abre tu navegador en `http://127.0.0.1:5000`

## Funcionalidades Principales

- **Procesamiento de Datos**: Cálculo dinámico de promedios, tasas de reprobación y alumnos en riesgo utilizando Pandas.
- **Visualización**: Tablero interactivo con métricas clave y listado de alumnos críticos.
- **Arquitectura**: Separación de lógica (Backend) y presentación (Frontend) siguiendo el patrón MVC.
