import sys
import os

sys.path.append(os.getcwd())

from django.utils import timezone
import datetime
import time
import threading
import subprocess

from jobs.core.main import setup_logger
from jobs.core.sec.main import crypto_file
from jobs.models import Crontab as CrontabModel, ExecutionLog, ExecutionManual, Scripts
from jobs.core.application.main import RunAll as internalRoutines

log = setup_logger('core')

sem = threading.Semaphore(20)

c = crypto_file(loadFile=True)
c.config()

env = {
    **os.environ,
    'PYTHONPATH': os.getcwd()
}

def run(script):

    sem.acquire()
    log.info('process ' + script + ' started')
    try:
        sub = subprocess.check_output('python jobs/scripts/' + script, env=env, stderr=subprocess.STDOUT)
        log.info('process ' + script + ' success')
    except subprocess.CalledProcessError as e:
        log.error(e.output)

    sys.stdout.flush()
    sem.release()

def run2Django(script, idScript, idCrontab, arguments:str=''):

    if arguments is None:
        arguments = ' '

    execLog = ExecutionLog.objects.filter(
        script_id = idScript
        , crontab_id = idCrontab
        , success = 0
        , createdAt__gte = timezone.now() - timezone.timedelta(hours=6)
        , startedAt = None
        , finishedAt = None)

    if execLog and idCrontab is not None:
        execLog = ExecutionLog(
            script_id=idScript
            , crontab_id=idCrontab
            , startedAt = timezone.now()
            , finishedAt=timezone.now()
            , success=0
            , message='Sobreposição de tarefas, verificar possivel lentidão ou aumentar o tempo de execução')
        execLog.save()
        return 0


    execLog = ExecutionLog(script_id=idScript,crontab_id=idCrontab)
    execLog.save()

    sem.acquire()
    log.info(f'process {script} started id script:{idScript} id crontab:{idCrontab}')
    execLog = ExecutionLog.objects.get(id=execLog.id)
    execLog.startedAt = timezone.now()
    log.info(f'arguments:{arguments}')
    log.info(f'python jobs/scripts/{script} {arguments}')
    try:
        subprocess.check_output(f'amb/Scripts/python.exe jobs/scripts/{script} {arguments}' , env=env, stderr=subprocess.STDOUT)
        log.info('process ' + script + ' success')
        execLog.success = True
    except subprocess.CalledProcessError as e:
        log.error(e.output)
        execLog.success = False
        execLog.message = e.output[-1000:]
        
    execLog.finishedAt = timezone.now()    
    execLog.save()

    sys.stdout.flush()
    sem.release()

class Crontab:

    def __init__(self):

        self.loadCrontabFile()

    def _crontabRegex(self,val,now=None,zfill=True):
        if (val.find('/') >= 0) and (val.find('-') >= 0):
            raise Exception('/ and - in same crontab not supported')
        elif val == '*':
            if zfill:
                now = str(now).zfill(2)
                return now
            else:
                return str(now)
        elif val.find('/') > 0:
            start, v = val.split('/')
            start = int(start)
            v = int(v)
            now = int(now)
            if (int(start) < now) & (now % v == 0):
                if zfill:
                    now = str(now).zfill(2)
                    return now
                else:
                    return str(now)
        elif val.find('-') > 0:
            start, end = val.split('-')
            start = int(start)
            end = int(end)
            now = int(now)
            if now in range(start,end+1):
                if zfill:
                    now = str(now).zfill(2)
                    return now
                else:
                    return str(now)
        else:
            try:
                val = int(val)
                now = int(now)
                if val == now:
                    if zfill:
                        now = str(now).zfill(2)
                        return now
                    else:
                        return str(now)
            except:
                pass
        return '99'

    def checkMinute(self):
        now = datetime.datetime.now().strftime('%M')
        self.minute = self._crontabRegex(val=self.minute,now=now)

    def checkHour(self):
        now = datetime.datetime.now().strftime('%H')
        self.hour = self._crontabRegex(val=self.hour,now=now)
        
    def checkDayOfMonth(self):
        now = datetime.datetime.now().strftime('%d')
        self.dayOfMonth = self._crontabRegex(val=self.dayOfMonth,now=now)

    def checkMonth(self):
        now = datetime.datetime.now().strftime('%m')
        self.month = self._crontabRegex(val=self.month,now=now)

    def checkDayOfWeek(self):
        now = datetime.datetime.now().strftime('%w')
        self.dayOfWeek = self._crontabRegex(val=self.dayOfWeek,now=now,zfill=False)        

    def checkCron(self):
        self.checkMinute()
        self.checkHour()
        self.checkDayOfMonth()
        self.checkMonth()
        self.checkDayOfWeek()

        check = self.minute + self.hour + self.dayOfMonth + self.month + self.dayOfWeek
        log.debug('valor cron:' + check + ' hora atual:' + datetime.datetime.now().strftime('%M%H%d%m%w'))
        if check == datetime.datetime.now().strftime('%M%H%d%m%w'):
            return True
    
    def loadCron(self,cron):
        self.cron = cron
        self.cronTime = self.cron.split(' ')[:5]
        self.minute = self.cronTime[0]
        self.hour = self.cronTime[1]
        self.dayOfMonth = self.cronTime[2]
        self.month = self.cronTime[3]
        self.dayOfWeek = self.cronTime[4]

        self.job = ' '.join(self.cron.split(' ')[5:])

        log.debug(self.cronTime)
        return self.checkCron()

    def loadCrontabFile(self,file='media/crontab.tab'):

        f = open(file,'r')
        f1 = f.readlines()
        f.close()
        nl = []
        for i in f1:
            if i.startswith('#'):
                continue
            elif i.startswith('\n'):
                continue
            elif i.startswith(' '):
                continue
            
            if not os.path.isfile('scripts/' + i.split()[5]):
                raise Exception('file ' + 'scripts/' + i.split()[5] + ' not found.')

            nl.append(i.replace('\n',''))

        self.cronJobs = nl

    def executeCron(self):
        while True:
            now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
            now4thread = datetime.datetime.now().strftime('%Y%m%d%H%M')
            print('executando:',now)

            if threading.active_count() > 1:
                log.info('active threads -> ' + str(threading.active_count()))
                for thread in threading.enumerate():
                    log.info('thread name-> ' + thread.name)
            
            for job in self.cronJobs:
                log.debug('job:' + job)
                if self.loadCron(job):
                    log.info('send to queue -> ' + self.job)
                    t = threading.Thread(target=run,name= self.job + '_' + now4thread,args=(self.job,))
                    t.start()
            
            time.sleep(60)


class Crontab2Django(Crontab):

    def loadCrontabFile(self):
        scripts = Scripts.objects.filter(active=True)
        cron = CrontabModel.objects.filter(active=True,script__in=scripts)
        l = []
        for c in cron:
            l.append({'file':f'{c.minute} {c.hour} {c.dayOfMonth} {c.month} {c.dayOfWeek} {c.script.script}'
                    ,'script':c.script.id
                    ,'crontab':c.id
                    ,'arguments':c.arguments})
        
        self.cronJobs = l

    def onlyExec(self):

        self.loadCrontabFile()
        now4thread = timezone.now().strftime('%Y%m%d%H%M')
        print(now4thread)

        if threading.active_count() > 1:
            log.info('active threads -> ' + str(threading.active_count()))
            for thread in threading.enumerate():
                log.info('thread name-> ' + thread.name)
        
        for job in self.cronJobs:
            log.debug('job:' + job.get('file'))
            if self.loadCron(job.get('file')):
                log.info('send to queue -> ' + self.job)
                t = threading.Thread(target=run2Django
                                    , name= self.job + '_' + now4thread
                                    , args=(self.job, job.get('script'), job.get('crontab'), job.get('arguments')))
                t.start()
        
        manual = ExecutionManual.objects.filter(run=True,startAt__lte=timezone.now(),finishedAt=None).exclude(user=0)
        for m in manual:
            script = Scripts.objects.filter(id=m.script.id,active=True)
            if script:
                scr = script[0].script
                idScript = script[0].id
                arguments = m.arguments
                idCrontab = None
                log.info('send to queue manual-> ' + scr)
                t = threading.Thread(target=run2Django
                                    , name= scr + '_' + now4thread
                                    , args=(scr, idScript, idCrontab, arguments))
                t.start()
                manual = ExecutionManual.objects.get(id=m.id)
                manual.finishedAt = timezone.now()
                manual.run = False
                manual.save()
                                                  

    def executeCron(self):

        internalRoutines()

        ExecutionLog.objects.filter(
            startedAt=None
            , finishedAt=None
            , success = 0
            ).update(
                startedAt=timezone.now()
                , finishedAt=timezone.now()
                , message = '[Zumbi] - Processo não executado.'
        )
        while True:
            self.onlyExec()
            time.sleep(60)
            if datetime.datetime.now().strftime('%d%H%M') == '150100':
                log.info('executando rotinas internas')
                internalRoutines()



if __name__ == '__main__':

    internalRoutines()
    c = Crontab()
    c.executeCron()