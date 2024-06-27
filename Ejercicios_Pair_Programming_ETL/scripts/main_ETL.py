
import soporte_ETL1

#Llamo a la función de leer csv clientes.
df_clientes = soporte_ETL1.leer_csv('clientes.csv')
print('Las 5 primeras filas del DataFrame de CLIENTES son:\n')
print(df_clientes.head())
print('.....................................................')

#Llamo a la función para ver la info del DF clientes.
print('Las información del DataFrame de CLIENTES es:\n')
print(soporte_ETL1.info_df(df_clientes))
print('.....................................................')


#Llamo a la función de leer csv ventas.
df_ventas = soporte_ETL1.leer_csv('ventas.csv') 
print('Las 5 primeras filas del DataFrame de VENTAS son:\n')
print(df_ventas.head())
print('.....................................................')


#Llamo a la función para ver la info del DF ventas.
print('Las información del DataFrame de VENTAS es:\n')
print(soporte_ETL1.info_df(df_clientes))
print('.....................................................')


#Llamo a la funcion para ver el csv de producto y convertir en DF.
df_productos = soporte_ETL1.leer_csv_productos('productos.csv')
print('Las 5 primeras filas del DataFrame de PRODUCTOS son:\n')
print(df_productos.head())
print('.....................................................')


#Llamo a la función para ver la info del DF ventas.
print('Las información del DataFrame de PRODUCTOS es:\n')
print(soporte_ETL1.info_df(df_productos))
print('.....................................................')


#Llamo a la función para cambiar el tipo de una columna del DF de productos.
df_productos = soporte_ETL1.convertir_precio_a_float(df_productos)


#Llamo a la función para gestionar los nulos categóricos del DF clientes.
df_clientes = soporte_ETL1.gestionar_nulos_categoricos(df_clientes)


#Llamo a la función para unir los 3 DF en DF tienda.
df_tienda= soporte_ETL1.unir_df(df_ventas, df_productos, df_clientes)
print('Las información del DataFrame de TIENDA es:\n')
print(df_tienda.head())
print('.....................................................')


#Llamo a la función para eliminar columnas duplicadas en DF tienda.
df_tienda= soporte_ETL1.eliminar_columnas_duplicadas(df_tienda)


#Llamo a la función para cambiar nombres columnas DF tienda.
df_tienda= soporte_ETL1.renombrar_columnas(df_tienda)


#Llamo a la función para igualar nombres DF tienda.
df_tienda= soporte_ETL1.igualar_nombres_columnas_titulo(df_tienda)


print('El DF tras la eliminación de columnas duplicadas e igualar los nombres queda así:\n')
print(df_tienda.head())
print('.....................................................')


#Llamo a la función para gestionar nulos categóricos DF tienda.
df_tienda= soporte_ETL1.gestionar_nulos_categoricos_tienda(df_tienda)


#Dudo de si tiene sentido llamar a la función para gestionar nulos numéricos de DF tienda por la ausencia notable de datos.
#df_tienda= gestionar_nulos_numericos(df_tienda)


#Compruebo que no quedan nulos.
#df_tienda.isnull().sum()


#Compruebo que todo está correcto.
print('El DF sin imputar los nulos numéricos ante las dudas que me genera por la falta de datos queda así:\n')
print(df_tienda.head())


#Llamo a la función para guardar DF tienda como csv.
soporte_ETL1.guardar_en_csv(df_tienda, 'tienda.csv')