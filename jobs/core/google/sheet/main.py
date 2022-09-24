from xmlrpc.client import Boolean
import apiclient.errors as errors
import os
import pandas as pd
from googleapiclient.http import MediaFileUpload


from jobs.core.sec.main import crypto_file
from jobs.core.google.main import Create_Service
from jobs.core.google.file.main import File
from jobs.core.log.logger import setup_logger

crypto = crypto_file()
config = crypto.config()

log = setup_logger('core')

class Sheet:

    def __init__(self,api_version='v4'):
        CLIENT_SECRET_FILE = ('client_secrets.json')
        API_NAME = 'drive' if api_version == 'v3' else 'sheets'
        self.API_VERSION = api_version
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE,API_NAME,self.API_VERSION,SCOPES)
        self.service = service

    def get(self,file:str,parents:str=None):
        '''
        get file metadata
        '''
        df = File()
        res = df.get(file=file,parents=parents)
        return res

    def create(self,file:str,parents:list=None,delete:bool=True):
        '''
        create new file
        '''
        if not os.path.exists(file):
            return 0

        if self.get(file=file) is None:
            try:
                if self.API_VERSION == 'v3':
                    file_metadata = {
                        'name': os.path.basename(file)
                        , 'mimeType': 'application/vnd.google-apps.spreadsheet'
                        , 'parents': parents
                    }

                    media = MediaFileUpload(filename=file, mimetype='text/csv')

                    response = self.service.files().create(
                        media_body=media,
                        body=file_metadata
                    ).execute()
                    return response
                elif self.API_VERSION == 'v4':

                    test_file = self.get(file)
                    if test_file:
                        return 0

                    spreadsheet = {
                        'properties': {
                            'title': file.split('/')[-1].split('.')[0]
                        }
                    }

                    spreadsheet = self.service.spreadsheets().create(body=spreadsheet,fields='spreadsheetId').execute()
                    self.update(file=file,parents=parents)
                    return spreadsheet
                
                if delete:
                    os.remove(file)

            except Exception as e:
                print(e)
                log.error(e)
                return False
        else:
            log.error(file + ' already exists, please, use method update')
            return False

    def update(self,file,parents:list=None,delete:bool=True):
        '''
        update file
        '''
        
        log.info('Updating file: ' + file)
        log.info(f'API version: {self.API_VERSION}')

        if not os.path.exists(file):
            return 0

        if self.API_VERSION == 'v3':
            files = self.get(file,parents)

            for f in files:

                try:
                    file_id = f.get('id')
                    media_body = MediaFileUpload(file, resumable=True)

                    updated_file = self.service.files().update(
                        fileId=file_id,
                        body=file,
                        media_body=media_body).execute()
                    return updated_file
                except errors.HttpError as e:
                    log.error(e)
                    return None
        elif self.API_VERSION == 'v4':
            name = file.split('/')[-1:][0]
            name = name.split('.')[0]

            fileId = self.get(file)
            if fileId is None:
                return False
            
            fileId = fileId[0].get('id')

            df = pd.read_csv(file)
            df.fillna('',inplace=True)

            values = []    
            values.append(df.keys().tolist())
            for v in df.values.tolist():
                values.append(v)
                

            body = {
                'values': values
            }

            value_input_option = 'RAW'

            self.clear(fileId=fileId)

            result = self.service.spreadsheets().values().update(
                spreadsheetId=fileId
                , range='Página1'
                , valueInputOption=value_input_option
                , body=body
            ).execute()

            if delete:
                os.remove(file)

            return result
    
    def clear(self,fileId,range='Página1'):
                
        result = self.service.spreadsheets().values().clear(
            spreadsheetId=fileId
            , range=range
        ).execute()

        return result

    def delete(self,file,folder):
        '''
        delete file
        '''
        pass