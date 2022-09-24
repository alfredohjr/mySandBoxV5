import os
from pandas import read_sql
from sqlalchemy import create_engine
import datetime as dt

from jobs.core.log.logger import setup_logger
from jobs.core.sec.main import crypto_file

crypto = crypto_file()
config = crypto.config()

log = setup_logger('core')

class sqltodf:

    def __init__(self,banco):
        log.debug('started')
        log.debug('db:' + banco)

        try:
            self.banco = config.get('db_' + banco.lower())
        except Exception as e:
            self.banco = None
            log.error('error:' + str(e))
        
        if self.banco == None:
            raise Exception('banco de dados ' + banco + ' invalido.')

        tipo, usuario, senha, instancia, *detalhes = self.banco.split(',')
        if tipo == 'oracle':
            eng = 'oracle+cx_oracle://{USER}:{PASS}@{SID}'.format(USER=usuario,PASS=senha,SID=instancia)
            self.eng = create_engine(eng)
        elif tipo == 'mysql':
            host = detalhes[0]
            eng = f'mysql+pymysql://{usuario}:{senha}@{host}/{instancia}'
            self.eng = create_engine(eng)

        os.environ['NLS_LANG'] = "AMERICAN_AMERICA.WE8ISO8859P1"

        self.data = dt.datetime.now().strftime('%Y%m%d')

    
    def execute(self,sql):
        log.debug('started sql')
        log.debug('sql: ' + sql)
        start = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        df = read_sql(sql,self.eng)
        end = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.debug('total lines:' + str(df.index.size) + ' X ' + str(len(df.keys())))
        log.debug('finished sql')

        df = _dataT(df)

        try:
            f = open('tmp/log/LOG_f_sqltodf_{}.log'.format(self.data),'a')
            f.write(f'<sql><data><start>{start}</start><end>{end}</end></data><sqlcommand>{sql}</sqlcommand><sql>\n')
            f.close()
        except:
            f = open('tmp/log/LOG_f_sqltodf_{}.log'.format(self.data),'a')
            f.write(f'<sql><data><start>{start}</start><end>{end}</end></data><sqlcommand>{sql}</sqlcommand><sql>\n')
            f.close()
        return df

    def executeFromFile(self,file,params=None):
        '''
        le um arquivo sql e retorna um dataframe,
        aceita um dicionario de parametros.
        '''

        sql = ''
        with open(file,'r') as file:
            sql = file.read()

        if params == None:
            return self.execute(sql)
        else:
            return self.execute(sql.format(**params))


def _dataT(df):

    if 'numcad' in df.keys():
        df['numcad'] = df['numcad'] + 857498357
    
    if 'numcpf' in df.keys():
        df['numcpf'] = df['numcpf'] + 548329487
    
    if 'numpis' in df.keys():
        df['numpis'] = df['numpis'] + 638724876
    
    return df