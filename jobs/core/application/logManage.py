import os
import datetime
import zipfile
import socket

from jobs.core.log.logger import setup_logger

log = setup_logger('core')

def run():
    path = 'tmp/log'
    yyyymm = datetime.datetime.now().strftime('%Y%m')

    data_list = []
    for file in os.listdir(path):
        if file.endswith('.log'):
            data = file.split('.')[0]
            data = data.split('_')[-1]
            data = data[:6]
            
            if not data.startswith('20'):
                continue
            
            if data == yyyymm:
                continue
            
            if data not in data_list:
                data_list.append(data)


    for data in data_list:

        datetime_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        file_zip = f'{path}/BkpLog_{socket.gethostname()}_{datetime_now}_{data}.zip'
        zipObj = zipfile.ZipFile(file_zip,'w')
        
        for file in os.listdir(path):
            
            if not file.endswith('.log'):
                continue
                
            data_check = file.split('.')[0]
            data_check = data_check.split('_')[-1]
            data_check = data_check[:6]
            if data_check == data:
                comp = zipfile.ZIP_BZIP2
                zipObj.write(f'{path}/{file}', arcname=file,compress_type=comp)
                try:
                    os.remove(f'{path}/{file}')
                except:
                    log.error(f'Erro ao remover arquivo {file}')
        
        zipObj.close()