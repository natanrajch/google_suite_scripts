from __future__ import print_function
import pickle
import os.path
import sigquery
import drive
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime, timedelta 

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def crear_sheets_service():
    """Conecta al servicio de sheets
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    return service

def reescribir_sheets(service,SPREADSHEET_ID,range_name,body,filas_actuales):
    """Escribe el body ({values: list of lists}) desde el range_name (estilo 'Hoja 1!A1') en la
     spreadsheet_ID. Requiere filas_actuales para borrarlas si son más que el body actual"""
    nuevas_filas = len(body['values'])
    #Extiende el rango de las nuevas filas para cubrir todo el 
    #rango de sheets. Te ahorras una call a la api de esta forma, 
    #aunque vuelve al archivo mas pesado.
    if nuevas_filas < filas_actuales: 
        fila_vacia = []
        nuevo_body = body['values']
        for col in body['values'][0]:
            fila_vacia.append('')
        for i in range(filas_actuales - nuevas_filas):
            nuevo_body.append(fila_vacia)
        body = {'values' : nuevo_body}
        
        
    result = service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID, range=range_name,
    valueInputOption="USER_ENTERED", body=body).execute()
    #print('{0} cells updated.'.format(result.get('updatedCells')))

def limpiar_filtros(service, SPREADSHEET_ID, nombre_hoja):
    """Quita filtros de toda la hoja. Alimentar Service de conexion a API, spreadsheet ID, y el nombre_hoja (estilo 'Hoja 1') como string.
    Hace 2 Calls. Una de lectura para encontrar cant. rows y una de escritura para quitar los fitros"""
    
    lectura = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID, ranges=nombre_hoja).execute()
    last_row = lectura['sheets'][0]['properties']['gridProperties']['rowCount']    
    last_column = lectura['sheets'][0]['properties']['gridProperties']['columnCount']   
    sheet_id = lectura['sheets'][0]['properties']['sheetId']   
    filter_settings = { 
    "range": {
    "sheetId": sheet_id,
    "startRowIndex": 0,
    "endRowIndex": last_row,
    "startColumnIndex": 0,
    "endColumnIndex": last_column
    }}
    
    sacarfiltros = {"requests":[{
        "setBasicFilter": {
            "filter": filter_settings}
            }]
        }

    service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=sacarfiltros ).execute()
    return filter_settings