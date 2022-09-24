import os
import time
from googleapiclient.http import MediaFileUpload

from jobs.core.google.main import Create_Service
from jobs.core.sec.main import crypto_file

crypto = crypto_file()
config = crypto.config()

class File:

    def __init__(self):
        CLIENT_SECRET_FILE = ('client_secrets.json')
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
        self.service = service
    
    def get(self, file:str, parents:str=None):
        
        page_token = None
        files = []
        file = file.split('/')[-1]
        file = '.'.join(file.split('.')[:-1])

        while True:
            response = self.service.files().list(q="name='{FILE}'".format(FILE=file)
                                                , spaces='drive'
                                                , fields='nextPageToken, files(id, name)'
                                                , pageToken=page_token).execute()

            for f in response.get('files', []):
                files.append({'name':f.get('name'),'id':f.get('id')})
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        if not files:
            return None

        return files

    def create(self, file, parents:list=None, delete:bool=True):
        file_metadata = {
              'name': os.path.basename(file)
            , 'parents': parents
            }

        media = MediaFileUpload(filename=file)

        response = self.service.files().create(
                    media_body=media,
                    body=file_metadata
                ).execute()
        
        if delete:
            try:
                os.remove(file)
            except:
                pass

        return response