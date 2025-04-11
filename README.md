# Manual de uso - Fase 3

## Requisitos

- Python 
- PostgreSQL  
- psycopg2 (instalar con `pip install psycopg2`)

## Pasos para ejecutar la simulación

1. Clonar este repositorio o descargar el archivo `fase3.py`.  
2. Instalar la librería psycop2
3. Editar los datos de conexión a la base de datos local en la variable `BD` dentro de `fase3.py`:
    BD = {
        "dbname": "nombre_de_tu_bd",
        "user": "tu_usuario",
        "password": "tu_contraseña",
        "host": "localhost",
        "port": 5432
    }
4. Cambiar el nivel de aislamiento en la variable AISLAMIENTO para probar los distintos niveles:
    Ej: AISLAMIENTO = "READ COMMITTED"
5. Cambiar el número de asiento si quiere probar con otro:
    ASIENTO = 10
6. Ejecutar el programa en la terminal o en VS:
    python fase3.py
7. Ingresar el número de usuarios para la simulación cuando se solicite