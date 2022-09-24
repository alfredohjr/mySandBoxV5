from jobs.core.google.main import Create_Service
from jobs.core.log.logger import setup_logger
from jobs.core.sec.main import crypto_file

crypto = crypto_file()
config = crypto.config()

log = setup_logger('core')

class Folder:

    def __init__(self):
        CLIENT_SECRET_FILE = ('client_secrets.json')
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)
        self.service = service

    def get(self, name:str):
        response = self.service.files().list(
            q = f"name='{name}'"
            , spaces = 'drive'
            , fields = 'nextPageToken, files(id, name)'
        ).execute()

        if response.get('files'):
            return response.get('files')[0].get('id')

    def create(self, name:str, parents:list=None):

        if self.get(name):
            return 0

        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        if parents:
            file_metadata['parents'] = [parents]

        response = self.service.files().create(body=file_metadata,fields='id').execute()
        return response.get('id')

    def move(self,fileId,parent=None,parentsId=None):

        log.info(f'fileId:{fileId}, parent:{parent}, parentsId:{parentsId}')

        if not fileId:
            return 0

        if parent:
            parentsId = self.get(name=parent)

        if parentsId is None:
            log.info('ParentId is None, exit.')

        result = self.service.files().update(
                                    fileId=fileId,
                                    addParents=parentsId,
                                    fields='id, parents').execute()
        return result

