'''
    Criado por: Alfredo Holz Junior
    Email: alfredojrgasper@gmail.com
    
    Objetivo do script: Arquivo de configuração central de todos os
        scripts.
        
    Melhorias:
'''

from jobs.core.main import setup_logger
from jobs.core.sec.main import crypto_file

crypto = crypto_file()
config = crypto.config()

fr_baseurl = config.get('fr_baseurl')
fr_token = config.get('fr_token')

path_scripts = config.get('path_home','jobs/scripts')
path_tmp = config.get('path_tmp','tmp')

telegram_key = config.get('telegram_key')
telegram_message = config.get('telegram_message')

admin_email = config.get('admin_email')
admin_pass = config.get('admin_pass')
email_port = config.get('email_port')
email_serv = config.get('email_serv')
email_from = config.get('email_from')

bovespa_db = config.get('bovespa_db','bovespa.db.sqlite3')