#!/usr/bin/env python
import os
import sigquery
import drive
import sheets
from datetime import datetime, timedelta 
import pandas as pd
import numpy as np

#Maneja diferencia horaria del server linux (3hs) y del server Drive
is_windows = os.name == 'nt'
diferencia_hor = timedelta(hours=0) if is_windows else timedelta(hours=3)
ahora = datetime.now() - diferencia_hor

#Query SQL
sql_query = """UN QUERY SQL"""
values = sigquery.query_a_sig(sql_query)

#Filtrado de datos
df = pd.DataFrame.from_records(values)
df.columns = ['Lista', 'de', 'columnas']
condiciones = [df['Lista'] == '1',df['de'] == '1', 
               df['condiciones'] == '1']
tipos = ['Lista', 'de', 'tipos']

df['Tipo'] = np.select(condiciones,tipos)
df_miserere = df.loc[df['Condicion'] == 'Plaza Miserere'][['Lista','de','columnas']].copy()
df_miserere['Reclamo'] = 'Reclamo abierto'

#Seteo de datos a formato google sheets
df_miserere = df_miserere.applymap(str)
values = df_miserere.to_numpy().tolist()

#Agregar encabezado con hora de ultima modificacion
encabezado = ['actualizado '+ahora.strftime("%d/%m/%Y %H:%M"), 'Tipo','=SI(C2="";"Ningún medio de elevación tiene reclamo abierto";"ID - Detalle")', 'Reclamo']
values.insert(0, encabezado) 

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'ID del spreadsheet'


#Si el archivo no fue modificado en más de 7 min, hace query, limpia los filtros y actualiza la data

service = sheets.crear_sheets_service()

#Crea el body de valores para escribir en sheets mediante la API
body = {
'values': values
}
range_name = 'Reclamos abiertos!A1' #Escribir a partir de esta celda
filtros = sheets.limpiar_filtros(service,SPREADSHEET_ID,'Reclamos abiertos') #limpia filtros y devuelve cant total de filas
filas_actuales = filtros['range'].get('endRowIndex')

sheets.reescribir_sheets(service,SPREADSHEET_ID,range_name,body,filas_actuales)
print('actualizar_sig_sheets.py ejecutado a las {0}.'.format(ahora))