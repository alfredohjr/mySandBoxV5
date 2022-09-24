import os
import datetime

from jobs.core.application.sqlite3ManageTables import RunAll as BackupTables
from jobs.core.application.sqlite3BackupJobs import RunAll as BackupJobs
from jobs.core.application.logManage import run as BackupLogs


def RunAll():

    now = datetime.datetime.now().strftime('%Y%m%d')

    if not os.path.isfile(f'tmp/bkp_{now}.log'):
        BackupTables()
        BackupJobs()
        BackupLogs()

        f = open(f'tmp/bkp_{now}.log','w')
        f.write(f'{now}')
        f.close()

if __name__ == "__main__":
    RunAll()