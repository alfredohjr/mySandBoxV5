import subprocess
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import datetime
import os
import time

path = 'c:/dados/trabalho/mySandBoxV5'
port = 8000

svc_name_ = "mySandBoxV5"
svc_display_name_ = "mySandBox"
svc_description_ = "Scripts for all"

os.chdir(path)

env = {
    **os.environ,
    'PYTHONPATH': path
}

hora = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = 'pythonService'
    _svc_display_name_ = 'Python Service'
    _svc_description_ = 'Python Service Description'

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        '''
        Main class to be ovverridden to add logic
        '''
        pass


class PythonService(SMWinservice):
    _svc_name_ = svc_name_
    _svc_display_name_ = svc_display_name_
    _svc_description_ = svc_description_

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        
        created = False
        while self.isrunning:

            if not created:
                try:
                    
                    os.chdir(path)
                    subprocess.Popen(f'amb\Scripts\python.exe manage.py runserver 0.0.0.0:{port}', shell=True)
                    subprocess.Popen('amb\Scripts\python.exe manage.py runscript runCrontab', shell=True)

                    created = True
                except subprocess.CalledProcessError as e:
                    f = open('tmp/Service.log','a')
                    f.write(f'[ERROR] - {e.output}\n')
                    f.close()

            time.sleep(1)
            
        subprocess.call(['taskkill','/IM','python.exe','/F'])         
        

if __name__ == '__main__':
    PythonService.parse_command_line()