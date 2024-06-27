
"""En este caso trabajas en una empresa de venta al por menor de productos italianos y debes realizar la limpieza,
transformación e integración de datos de ventas, productos y clientes para su análisis.
Los pasos que deberás seguir en este ejercicio son:

1. Lectura de la Información:
    - Leer los archivos CSV (ventas.csv, productos.csv, clientes.csv).
    - Explorar los conjuntos de datos para comprender su estructura, columnas, tipos de datos, etc.

2. Transformación de Datos:
    - Limpiar los datos: manejar valores nulos, eliminar duplicados si los hay, corregir errores tipográficos, etc.
    - Aplicar transformaciones relevantes según sea necesario: por ejemplo, convertir tipos de datos, renombrar columnas, 
    crear nuevas características derivadas, etc.
"""

#Importo librerías
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import scipy.stats as stats
import scipy.stats as st
from scipy.stats import shapiro, poisson, chisquare, expon, kstest

import os
import sys
sys.path.append("../")

import warnings
warnings.filterwarnings("ignore")

"""........................................................................."""


"""Creo función para abrir csv, convertir en DF e imprmir info.
"""

def leer_csv(ruta_csv):
    df= pd.read_csv(ruta_csv)
    pd.set_option('display.max_columns', None)
    return df

def info_df(df):
    return df.info()


"""Creo función para abrir el csv de producto y convertir en DF.
"""
def leer_csv_productos(ruta_csv, sep='\t'):
    df_productos = pd.read_csv(ruta_csv, sep=sep)
    df_productos = df_productos.iloc[:, 0].str.split(',', expand=True)
    df_productos.columns = ['ID', 'Nombre_Producto', 'Categoría', 'Precio', 'Origen', 'Descripción', 'D1', 'D2', 'D3', 'D4']
    df_productos['Descripción'] = df_productos['Descripción'].fillna('') + \
                                  df_productos['D1'].fillna('') + \
                                  df_productos['D2'].fillna('') + \
                                  df_productos['D3'].fillna('') + \
                                  df_productos['D4'].fillna('')

    df_productos.drop(columns=['D1', 'D2', 'D3', 'D4'], inplace=True)
    df_productos['Descripción'] = df_productos['Descripción'].str.split('.').str[0]

    return df_productos


"""Creo función para cambiar el tipo de una columna del DF de producto."""

def convertir_precio_a_float(df_productos):
        df_productos['Precio'] = df_productos['Precio'].astype(float)
        return df_productos

"""Creo función para gestionar nulos categóricos DF clientes.
"""

def gestionar_nulos_categoricos(df_clientes):
    nulos_categoricos = df_clientes[df_clientes.columns[df_clientes.isnull().any()]].select_dtypes(include='O').columns
    
    for columna in nulos_categoricos:
        print(f"La distribución de las categorías para la columna {columna.upper()}")
        print(df_clientes[columna].value_counts() / df_clientes.shape[0])
        print("........................")
    
    # Imputar 'Unknown' en las columnas 'email', 'gender', 'City' y 'Address'
    df_clientes[['email', 'gender', 'City', 'Address']] = df_clientes[['email', 'gender', 'City', 'Address']].fillna('Desconocido')
    
    # Imputar 'Spain' en la columna 'Country'
    df_clientes['Country'] = df_clientes['Country'].fillna('Spain')
    
    return df_clientes


"""Creo función para unir los 3 DF sin perder registros de ninguno, usando outer.
"""

def unir_df(df_ventas, df_productos, df_clientes):
    df = df_ventas.merge(df_productos, left_on='ID_Producto', right_on='ID', how='outer')
    print(f"Tamaño después de unir ventas con productos: {df.shape}")
  
    df_tienda = df.merge(df_clientes, left_on='ID_Cliente', right_on='id', how='outer')
    print(f"Tamaño después de unir con clientes: {df_tienda.shape}")
    
    df_tienda.info()
    
    return df_tienda

"""Creo función para eliminar columnas duplicadas DF tienda.
"""

def eliminar_columnas_duplicadas(df_tienda):
    df_tienda.drop(columns=['ID_Cliente', 'ID'], inplace=True)    
    return df_tienda


"""Creo función para cambiar nombres columnas DF tienda.
"""
def renombrar_columnas(df_tienda):
    df_tienda.rename(columns={
    'id':'Id_Cliente',
    'first_name': 'Nombre_Cliente',
    'last_name': 'Apellido_cliente',
    'gender': 'Género',
    'City': 'Ciudad',
    'Country': 'País',
    'Address': 'Dirección'
}, inplace=True)

    return df_tienda


"""Creo función para igualar nombres columnas DF tienda.
"""
def igualar_nombres_columnas_titulo(df_tienda):
    df_tienda.columns = df_tienda.columns.str.title()
    return df_tienda


"""Creo función para gestionar nulos categóricos DF tienda.
"""
def gestionar_nulos_categoricos_tienda(df_tienda):
    # Seleccionar las columnas con nulos categóricos
    nulos_categoricos = df_tienda[df_tienda.columns[df_tienda.isnull().any()]].select_dtypes(include='O').columns
    
    # Imprimir las columnas con nulos categóricos
    print("Columnas con nulos categóricos:")
    print(nulos_categoricos)
    print("\n")
    
    # Calcular la distribución de los valores únicos dentro de las columnas que tienen nulos
    for columna in nulos_categoricos:
        print(f"La distribución de las categorías para la columna {columna.upper()}:")
        print(df_tienda[columna].value_counts() / df_tienda.shape[0])
        print("........................")
    
    # Imputar la moda en las columnas 'País' y 'Origen'
    pais_moda = df_tienda['País'].mode()[0]
    df_tienda['País'].fillna(pais_moda, inplace=True)
    
    origen_moda = df_tienda['Origen'].mode()[0]
    df_tienda['Origen'].fillna(origen_moda, inplace=True)
    
    # Imputar 'Desconocido' en el resto de columnas con nulos categóricos
    columnas_a_imputar_desconocido = ['Dirección', 'Ciudad', 'Género', 'Apellido_Cliente', 'Nombre_Cliente', 
                                      'Descripción', 'Categoría', 'Nombre_Producto']
    df_tienda[columnas_a_imputar_desconocido] = df_tienda[columnas_a_imputar_desconocido].fillna('Desconocido')
    
    # Imprimir el total de nulos después de la imputación
    print("Total de nulos después de la imputación:")
    print(df_tienda.isnull().sum())
    
    return df_tienda


"""Creo función para gestionar nulos numéricos DF tienda.
"""
def gestionar_nulos_numericos(df):
    nulos_numericos = df_tienda[df_tienda.columns[df_tienda.isnull().any()]].select_dtypes(include=np.number).columns
    print("Columnas con nulos numéricos:")
    print(nulos_numericos)
    print("\n")
    for columna in nulos_numericos:
        print(f"La distribución de los valores para la columna {columna.upper()}:")
        print(df_tienda[columna].value_counts() / df.shape[0])
        print("........................")
    
    for columna in nulos_numericos:
        mediana = df_tienda[columna].median()
        df_tienda[columna].fillna(mediana, inplace=True)
    
    df_tienda = df_tienda.dropna(subset=['Id_Cliente'])


"""Creo función para comprobar que no queden nulos.
"""
def comprobar_nulos(df_tienda):
    nulos_por_columna = df_tienda.isnull().sum()
    print("Número de nulos por columna:")
    print(nulos_por_columna)

"""Creo función para guardar el DF tienda.
"""

def guardar_en_csv(df_tienda, ruta_csv):
        df_tienda.to_csv(ruta_csv, index=False)
        print(f"DataFrame guardado exitosamente en: {ruta_csv}")


"""........................................................................."""

