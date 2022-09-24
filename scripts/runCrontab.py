from jobs.core.crontab.main import Crontab2Django
import sys

def run(*args):
    c = Crontab2Django()
    if 'execute' in args:
        c.onlyExec()
    else:
        c.executeCron()