
#Configuro la visualización del DF.
pd.set_option('display.max_columns', None)

#%%
#Abro el DF de ventas.
df_ventas= pd.read_csv('ventas.csv')
df_ventas.head()

#%%
#Imprimo la info básica. veo que no hay nulos y que las columnas son del tipo que le corresponde a cada una.
df_ventas.info()

#%%
#Abro el DF de clientes.
df_clientes= pd.read_csv('clientes.csv')
df_clientes.head()

#%%
#Imprimo la info básica. Observo que hay varias columnas categóricas con nulos.
df_clientes.info()

#%%
#Selecciono las columnas con nulos categóricos.
nulos_categoricos = df_clientes[df_clientes.columns[df_clientes.isnull().any()]].select_dtypes(include = "O").columns
nulos_categoricos

#%%
#Calculo como están distribuídos los valores únicos dentro de las columnas que tienen nulos.
for columna in nulos_categoricos:
    print(f"La distribución de las categorías para la columna {columna.upper()}")
    print(df_clientes[columna].value_counts() / df_clientes.shape[0])
    print("........................")

#%%
#Salvo en la columna country, al resto de nulos imputaré el valor 'Unknown'.
df_clientes['Country']= df_clientes['Country'].fillna('Spain')

df_clientes[['email', 'gender', 'City', 'Address']] = df_clientes[['email', 'gender', 'City', 'Address']].fillna('Desconocido')

#%%
#Compruebo que no haya nulos
df_clientes.isnull().sum()

#%%
#Abro el DF de productos. 
#Como me daba problemas al abrilo la columna descripción, uso otro delimitador de las columnas, en lugar de las comas, los tabuladores.
df_productos = pd.read_csv('productos.csv', sep='\t')

#Divido la única columna que me devuelve en varias columnas usando la coma como separador
df_productos = df_productos.iloc[:, 0].str.split(',', expand=True)

#Reasigno los nombres de las columnas, creando columnas nuevas que uniré a continuación.
df_productos.columns = ['ID', 'Nombre_Producto', 'Categoría', 'Precio', 'Origen', 'Descripción', 'D1', 'D2', 'D3', 'D4']

df_productos.head()

#%%
#Creo una nueva columna descripción y sumo los valores de las otras columnas.
#Imputo los nulos como valores vacíos ya que no me interesan.
df_productos['Descripción'] = df_productos['Descripción'].fillna('') + \
                                     df_productos['D1'].fillna('') + \
                                     df_productos['D2'].fillna('') + \
                                     df_productos['D3'].fillna('') + \
                                     df_productos['D4'].fillna('')
#Borro las columnas que ya no necesito.
df_productos.drop(columns=['D1', 'D2', 'D3', 'D4'], inplace=True)

#%%
#Como en la descripicón había informacíon duplicada la elimino y me quedo solo con la información que me interesa.
df_productos['Descripción'].str.split('.').str[0]

#%%
#Compruebo que la columna esté correcta.
list(df_productos['Descripción'])

#%%
#Sigo limpiando este DF de producto. Compruebo el tipo de las columnas.
df_productos.dtypes

#%%
#Cambio la columna de precio a float
df_productos['Precio']=df_productos['Precio'].astype(float)

#%%
#Compruebo que se ha ejecutado el cambio.
df_productos.dtypes

#%%
#Imprimo este DF que ya está limpio.
df_productos.head()

#%%
""" 3. Uno los tres DF ahora que ya están limpios a falta de igualar el nombre de las columnas 
y eliminar aquellas que se dupliquen.
"""

#%%
#Antes de seguir limpiando los DF, los uno. Comrpuebo la forma de cada uno.
print(f'Forma DF Productos: {df_productos.shape}')
print(f'Forma DF Ventas: {df_ventas.shape}')
print(f'Forma DF Clientes: {df_clientes.shape}')

print(df_productos.columns)
print(df_ventas.columns)
print(df_clientes.columns)


#%%
#Comparo los ID's de los dos DF por si puedo completar la info de ventas con la info de producto pero no.
id_productos_en_ventas = df_ventas['ID_Producto'].unique()
id_productos_en_productos = df_productos['ID'].unique()

count_no_encontrados = 0

for id_producto in id_productos_en_ventas:
    if id_producto not in id_productos_en_productos:
        count_no_encontrados += 1

print(f"Número de IDs de productos en df_ventas no encontrados en df_productos: {count_no_encontrados}")


#%%
#Comienzo uniendo el de ventas con productos, con un outer, para conservar todas las ventas y toda la info de producto.
df = df_ventas.merge(df_productos, left_on='ID_Producto', right_on='ID', how='outer')
print(df.shape)

#%%
#Imprimo la info y observo que están todos los datos
df.info()

#%%
#Uno el DF de clientes también con un outer para no perder información.
df_tienda = df.merge(df_clientes, left_on='ID_Cliente', right_on='id', how='outer')
print(df_tienda.shape)

#%%
#Imprimo la info para ver que todo esté correcto.
df_tienda.info()

#%%
#Borro las columnas duplicadas.
df_tienda.drop(columns=['ID_Cliente', 'ID'], inplace=True)


#%%
#Igualo el idioma de las columnas dado que algunas están en castellano y otras en inglés.
df_tienda.rename(columns={
    'id':'Id_Cliente',
    'first_name': 'Nombre_Cliente',
    'last_name': 'Apellido_cliente',
    'gender': 'Género',
    'City': 'Ciudad',
    'Country': 'País',
    'Address': 'Dirección'
}, inplace=True)


#%%
#Imprimo la info para ver que todo esté correcto.
df_tienda.info()


#%%
#Igualo el nombre de las columnas.
df_tienda.columns = df_tienda.columns.str.title()
df_tienda.columns

#%%
#Compruebo de nuevo los nulos, que entiendo que abrá ya que las tres tablas no tenían la misma longitud.
df_tienda.isnull().sum()

#%%
#Selecciono las columnas con nulos categóricos.
nulos_categoricos = df_tienda[df_tienda.columns[df_tienda.isnull().any()]].select_dtypes(include = "O").columns
nulos_categoricos

#%%
#Calculo como están distribuídos los valores únicos dentro de las columnas que tienen nulos.
for columna in nulos_categoricos:
    print(f"La distribución de las categorías para la columna {columna.upper()}")
    print(df_tienda[columna].value_counts() / df_tienda.shape[0])
    print("........................")


#%%
#En dos columnas, Origen y País imputo la moda.
pais_moda = df_tienda['País'].mode()[0]  # Calcula la moda y toma el primer valor si hay múltiples modas
df_tienda['País'].fillna(pais_moda, inplace=True)

origen_moda = df_tienda['Origen'].mode()[0]  # Calcula la moda y toma el primer valor si hay múltiples modas
df_tienda['Origen'].fillna(origen_moda, inplace=True)


#%%
#Al resto los imputo en la categoría desconocido.
df_tienda[['Dirección', 'Ciudad', 'Género', 'Apellido_Cliente', 'Nombre_Cliente', 'Descripción', 'Categoría', 'Nombre_Producto']] = df_tienda[['Dirección', 'Ciudad', 'Género', 'Apellido_Cliente', 'Nombre_Cliente', 'Descripción', 'Categoría', 'Nombre_Producto']].fillna('Desconocido')

#%%
df_tienda.isnull().sum()

#%%
#Selecciono las columnas con nulos numéricos.
nulos_numericos = df_tienda[df_tienda.columns[df_tienda.isnull().any()]].select_dtypes(include=np.number).columns
nulos_numericos

#%%
#Calculo como están distribuídos los valores únicos dentro de las columnas que tienen nulos.
for columna in nulos_numericos:
    print(f"La distribución de las categorías para la columna {columna.upper()}")
    print(df_tienda[columna].value_counts() / df_tienda.shape[0])
    print("........................")


#%%
#Como no hay ningún valor predominante en ningun producto, calculo medias y medianas.
print(df["Precio"].describe()[["mean", "50%"]])
print('.......................')
print(df["Total"].describe()[["mean", "50%"]])
print('.......................')
print(df["Cantidad"].describe()[["mean", "50%"]])


#%%
#Elimino los nulos en la columna Id_Cliente.
df = df.dropna(subset=['ID'])
