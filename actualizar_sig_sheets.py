#!/usr/bin/env python
import os
import sigquery
import drive
import sheets
from datetime import datetime, timedelta 



# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'ALGUN_ID'


#Obtiene fecha y hora de ultima modificacion

last_modified = drive.file_last_modified(SPREADSHEET_ID)
last_modified = datetime.strptime(last_modified, '%Y-%m-%dT%H:%M:%S.%fZ')
is_windows = os.name == 'nt'
#Se asume que drive siempre esta 3 horas adelantado. Pero en LINUX coincide la hora del sistema con drive.
last_modified = last_modified - timedelta(hours=3) 
diferencia_hor = timedelta(hours=0) if is_windows else timedelta(hours=3)
ahora = datetime.now() - diferencia_hor
delay = timedelta(minutes=7)
file_inactivo = (last_modified + delay) < ahora

#Si el archivo no fue modificado en más de 7 min, hace query, limpia los filtros y actualiza la data

if file_inactivo: 
    service = sheets.crear_sheets_service()
    sql_query = """UN QUERY SQL"""
    values = sigquery.query_a_sig(sql_query)

    #Agregar encabezado con hora de ultima modificacion
    encabezado = ['actualizado '+ahora.strftime("%d/%m/%Y %H:%M"), 'Nombres','de',
                    'columnas']
    values.insert(0, encabezado) 

    #Crea el body de valores para escribir en sheets mediante la API
    body = {
    'values': values
    }
    range_name = 'Hoja 1!A1' #Escribir a partir de esta celda
    filtros = sheets.limpiar_filtros(service,SPREADSHEET_ID,'Hoja 1') #limpia filtros y devuelve cant total de filas
    filas_actuales = filtros['range'].get('endRowIndex')
    
    sheets.reescribir_sheets(service,SPREADSHEET_ID,range_name,body,filas_actuales)
    print('actualizar_sig_sheets.py ejecutado a las {0}. Ult. modif era: {1}'.format(ahora, last_modified))
else:
    print('No ejecutado. Sheets en uso. Hora:{0}'.format(ahora))
