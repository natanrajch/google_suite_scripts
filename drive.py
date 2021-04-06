from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def file_last_modified(file_id):
    """Devuelve fecha de ultima modificacion del archivo de ID file_id
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokendrive.pickle'):
        with open('tokendrive.pickle', 'rb') as token:
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
        with open('tokendrive.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API - Devuelve listado dividido en paginas
    results = service.files().list( # pylint: disable=maybe-no-member
        pageSize=1000, fields="nextPageToken, files(id, modifiedTime)").execute()

    items = results.get('files', [])
    #print(items)   
    if not items:
        print('No se encuentra ningún archivo en el Service especificado')
    #Navega todas las paginas que a Drive se le ocurra darnos, mientras exista una proxima pagina
    while results.get('nextPageToken',[]):
        results = service.files().list( # pylint: disable=maybe-no-member
        pageToken=results.get('nextPageToken'), pageSize=1000, fields="nextPageToken, files(id, modifiedTime)").execute()     
        items.extend(results.get('files',[]))
    last_modified = next((item['modifiedTime'] for item in items if item["id"] == file_id),None)
    if last_modified:
        return last_modified
    else:
        print('No se encuentra el ID especificado en el Drive')
    
    # elif any([fileid not in item.values for item in items]):
    #     print('No se encuentra el fileid')
    #     print('Files:')
    #     for item in items:
    #         print(u'{0} ({1})'.format(item['id'],item['modifiedTime']))

if __name__ == '__main__':
    print(file_last_modified('el ID del FILE'))