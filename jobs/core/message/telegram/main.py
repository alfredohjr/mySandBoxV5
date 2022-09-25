from telebot import TeleBot
from dotenv import dotenv_values
from jobs.core.sec.main import crypto_file

crypto = crypto_file()
config = crypto.config()

def f_send_msg(msg,contato=None,isMarkdown=False):

    tel = Teleg(contact=contato)
    if isMarkdown:
        tel.send_markdown(message=msg)
    else:
        tel.send_message(message=msg)


class Teleg:

    def __init__(self,contact=None,key=None):
        if key == None:
            self.key = config.get('telegram_key')
        else:
            self.key = key
    
        print(config.get('telegram_key'))
        print(self.key)

        self.bot = TeleBot(self.key)
        if contact == None:
            self.contact = config.get('telegram_contact')
        else:
            self.contact = contact

    def send_message(self,message):
        self.bot.send_message(self.contact,message)

    def send_markdown(self,message):
        self.bot.send_message(self.contact,message,parse_mode='markdown')

    def send_document(self,file):
        f = open(file,'rb')
        self.bot.send_document(self.contact,f)

    def send_video(self,file):
        f = open(file,'rb')
        self.bot.send_video(self.contact,f)
    
    def send_photo(self,file):
        f = open(file,'rb')
        self.bot.send_photo(self.contact,f)