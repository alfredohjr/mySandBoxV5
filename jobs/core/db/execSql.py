from sqlalchemy import create_engine
import os
import datetime as dt

from jobs.core.log.logger import setup_logger
from jobs.core.sec.main import crypto_file

crypto = crypto_file()
config = crypto.config()

log = setup_logger('core')

class Execsql:
    '''
    Executa uma funcao dentro do banco, funciona com
    insert, update, delete e etc; procedures e coisas
    mais complexas não.
    '''

    def __init__(self,db):
        log.debug('started')
        log.debug('db:' + db)

        self.db = ''
        try:
            self.db = config.get('db_' + db.lower())
        except Exception as e:
            self.db = None
            log.error('error:' + str(e))
        
        if self.db == None:
            raise Exception('banco de dados ' + db + ' invalido.')

        tipo, usuario, senha, instancia = self.db.split(',')
        if tipo == 'oracle':
            eng = 'oracle+cx_oracle://{USER}:{PASS}@{SID}'.format(USER=usuario,PASS=senha,SID=instancia)
            self.eng = eng

        os.environ['NLS_LANG'] = "AMERICAN_AMERICA.WE8ISO8859P1"

        self.date = dt.datetime.now().strftime('%Y%m')
        self.con = create_engine(self.eng)


    def execute(self,command,data:list=None):
        """
        para executar mais de 1 update, passe os parametros da seguinte forma:
        command = 'update a set colunm = :v where column_b = :v2'
        data = [{'v': 1, 'v2': 'teste_1'}]
        """

        if data is None:
            self.con.execute(command)
        else:
            
            for d in data:
                self.con.execute(command,**d)
            
            self.con.execute('commit')