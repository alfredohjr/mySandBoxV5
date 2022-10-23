import pandas as pd
import datetime 
import sqlite3
import socket

from jobs.core.log.logger import setup_logger

log = setup_logger('core')

class Backup:

    def __init__(self, name):
        self.name = name
        self.dbFile = 'db.sqlite3'
        self.conn = sqlite3.connect(self.dbFile)
        self.key = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.file = f'tmp/csv/BKPForReport_{socket.gethostname()}_{self.name}_{self.key}.csv'
    
    def export(self):
        log.info(f'Exporting {self.name}')
        df = pd.read_sql(f"select * from {self.name}",con=self.conn)
        df.to_csv(self.file,index=None)

    def upload(self):
        pass
    
    def run(self):
        log.info(f'Exporting {self.name}')
        self.export()
        self.upload()


def RunAll():
    backups = [
        Backup('jobs_scripts'),
        Backup('jobs_crontab'),
    ]

    for backup in backups:
        backup.run()


if __name__ == '__main__':

    RunAll()