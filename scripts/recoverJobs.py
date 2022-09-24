from scripts.recoverCrontab import run as runCrontab
from scripts.recoverScript import run as runScript

def run(*args):
    runScript()
    runCrontab()