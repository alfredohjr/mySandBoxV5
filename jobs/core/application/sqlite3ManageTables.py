import pandas as pd
import datetime
import calendar
import os
import sqlite3
import socket

from jobs.core.log.logger import setup_logger

log = setup_logger('core')

class Table:

    def __init__(self, name, datetimeColumn, days):
        self.name = name
        self.datetimeColumn = datetimeColumn
        self.days = days
        self.dbFile = 'db.sqlite3'
        self.conn = sqlite3.connect(self.dbFile)

        self.date = datetime.datetime.now() - datetime.timedelta(days=days)
        self.date = f'{self.date.year}-{str(self.date.month).zfill(2)}-01 00:00:00'
    
    def export(self):
        log.info(f'Exporting {self.name}')
        df = pd.read_sql(f"select * from {self.name} where {self.datetimeColumn} <= '{self.date}'",con=self.conn)
        df[self.datetimeColumn] = pd.to_datetime(df[self.datetimeColumn])
        months = pd.value_counts(df[self.datetimeColumn].dt.strftime('%Y%m'))

        self.files = []
        self.months = []
        for month in months.index:
            log.info(f'Exporting {month}')
            key = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            lastDay = calendar.monthrange(int(month[0:4]),int(month[4:6]))[1]
            file = f'tmp/csv/BKPForReport_{socket.gethostname()}_{self.name}_{month}_{key}.csv'
            start = datetime.datetime(int(month[0:4]),int(month[4:6]),1)
            end = datetime.datetime(int(month[0:4]),int(month[4:6]),lastDay,23,59,59,999999)
            tmp = df[(df[self.datetimeColumn] >= start) 
                & (df[self.datetimeColumn] <= end)]
            tmp.to_csv(file,index=None)
            self.files.append(file)
            self.months.append([start,end])
            log.info(f'Exported {month}')

    def upload(self):
        pass

    def delete(self):
        log.info(f'Deleting {self.name}')
        for file in self.files:
            log.info(f'Deleting {file}')
            os.remove(file)
        
        for start, end in self.months:
            log.info(f'Deleting {start} - {end}')
            self.conn.execute(f"delete from {self.name} where {self.datetimeColumn} >= '{start}' and {self.datetimeColumn} <= '{end}'")
            self.conn.commit()

    def resizeDB(self):
        log.info(f'Resizing database')
        self.conn.execute('VACUUM')
        self.conn.commit()
        log.info(f'Resized database')

    def closeDB(self):
        log.info(f'Closing database')
        self.conn.close()
    
    def run(self):
        log.info(f'Running {self.name}')
        self.export()
        self.upload()
        self.delete()
        self.resizeDB()
        self.closeDB()
        log.info(f'Finished {self.name}')

def RunAll():
    tables = [
        Table('jobs_executionlog', 'createdAt', 30),
    ]

    for table in tables:
        table.run()

if __name__ == '__main__':

    RunAll()