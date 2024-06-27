## Ejercicios ETL I

Este proyecto automatiza las primeras dos fases del proceso de Extracción, Transformación y Carga (ETL) para la creación de un archivo CSV combinado llamado tienda, utilizando tres archivos CSV como fuente de datos.

### Estructura del proyecto**

- **main_ETL.py**: Este archivo contiene el script principal que ejecuta la ETL.
- **soporte_ETL.py**: Archivo de soporte donde se encuentran definidas las funciones utilizadas en el proceso ETL.

### Descripción de archivos
Archivos de entrada:
    - clientes.csv
    - productos.csv
    - ventas.csv

Archivo de salida:
    - tienda.csv: CSV combinado que resulta del proceso ETL.

### Funcionamiento
El archivo main_ETL.py hace uso de las funciones definidas en soporte_ETL.py para realizar las siguientes tareas:

1. Extracción: Leer los datos de los archivos CSV de clientes, productos y ventas.

2. Transformación: Aplicar transformaciones necesarias a los datos, como limpieza, normalización o combinación de tablas.

3. Carga: Escribir los datos transformados en el archivo tienda.csv.

### Ejecución
Para ejecutar el proceso ETL, asegúrate de tener instalado Python. Desde la línea de comandos, puedes ejecutar: \```bash
python main_ETL.py
\```