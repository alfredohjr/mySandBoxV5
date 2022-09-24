
from jobs.core.db.readSql import sqltodf
from jobs.core.db.execSql import Execsql
from jobs.core.db.execProc import ExecProc

from jobs.core.bi.format.df import df2Excel

from jobs.core.date.timeCourse import f_periodo_de_ate, f_periodo_v6

from jobs.core.google.sheet.main import Sheet
from jobs.core.google.file.main import File
from jobs.core.google.folder.main import Folder

from jobs.core.log.logger import setup_logger

from jobs.core.message.mail.main import Mail

from jobs.core.web.main import webScrapping


def f_sqltodf(sql,banco):
    s = sqltodf(banco)
    df = s.execute(sql)
    return df


def f_textodf(file,banco,parametros=None):
    s = sqltodf(banco)
    df = s.executeFromFile(file,params=parametros)
    return df


def f_execsql(sql,banco):
    f = Execsql(db=banco)
    f.execute(command=sql)


def f_execproc(banco,procedure,para_in,para_out=None):
    con = ExecProc(db=banco)
    con.execute(procedure=procedure,paramsIn=para_in,paramsOut=para_out)


def f_send_mail(titulo,mensagem,anexo=None,para=None):
    
    mail = Mail()
    mail.send(title=titulo,message=mensagem,attach=anexo,to=para)