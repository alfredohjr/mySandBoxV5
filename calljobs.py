import sys
import os
import subprocess
from jobs.core.log.logger import setup_logger
from jobs.core.sec.main import crypto_file
from jobs.core.application.main import RunAll as internalRoutines

c = crypto_file(loadFile=True)
c.config()

sys.path.append(os.getcwd())

env = {
    **os.environ,
    'PYTHONPATH': os.getcwd()
}

log = setup_logger('calljobs')

log.info(f'amb/Scripts/python.exe {sys.argv[1]} started')

internalRoutines()

try:
    sub = subprocess.check_output(f'amb/Scripts/python.exe {sys.argv[1]} {" ".join(sys.argv[2:])}', env=env, stderr=subprocess.STDOUT)
    log.info(f'process {sys.argv[1]} success')
except subprocess.CalledProcessError as e:
    log.error(e.output)

log.info(f'amb/Scripts/python.exe {sys.argv[1]} finished')
