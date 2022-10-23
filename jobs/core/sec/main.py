import os
from io import StringIO
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import argparse

isCrypto = False

class crypto:
    def __init__(self,key=None):
        if key is None:
            self._key = Fernet.generate_key()
        else:
            self._key = key
        
        self._f = Fernet(self._key)
    
    def set_text(self,text):
        return self._f.encrypt(text.encode())
        
    def get_text(self,text):
        return self._f.decrypt(text.encode()).decode()

class crypto_file:

    def __init__(self,loadFile=False):

        self.loadFile = loadFile
        if isCrypto:
            if os.environ.get('API_KEY') is None or os.environ.get('API_USER') is None:
                raise Exception('API_KEY e API_USER não definido, use -o generate para gerar um token')

            if os.environ.get('API_KEY'):
                self.crypto = crypto(key=os.environ.get('API_KEY'))
            
            if os.environ.get('API_USER'):
                pass
            else:
                pass
            self.file = '.env.crypto'

    def crypto_file(self,file):
        f = open(file,'r')
        f1 = f.readlines()
        f.close()

        f = open(self.file,'w')
        for line in f1:
            line = self.crypto.set_text(line)
            f.write(line.decode() + '\n')
        f.close()

    def decrypt_file(self,file):
        f = open(file,'r')
        f1 = f.readlines()
        f.close()

        for line in f1:
            line = self.crypto.get_text(line)
            if line.endswith('='):
                continue
            
            config = StringIO(line)
            load_dotenv(stream=config)

    def load_file(self,file):
        f = open(file,'r')
        f1 = f.readlines()
        f.close()

        for line in f1:
            if line.endswith('='):
                continue
            config = StringIO(line)
            load_dotenv(stream=config)
    
    def append_line(self,file):

        f = open('.env','r')
        f1 = f.readlines()
        f.close()

        env = dict()
        for line in f1:
            line = line.replace('\n','')
            line = self.crypto.get_text(line)
            k = line.split('=')[0]
            v = '='.join(line.split('=')[1:])
            env[k] = v.replace('\n','')
        
        f = open('.env.dec','w')
        for k,v in env.items():
            f.write(f'{k}={v}\n')
        f.close()

        f = open(file,'r')
        f1 = f.readlines()
        f.close()

        for line in f1:
            line = line.replace('\n','')
            k = line.split('=')[0]
            v = '='.join(line.split('=')[1:])
            env[k] = v

        f = open('.env', 'w')
        for k,v in env.items():
            line = f'{k}={v}'
            line = self.crypto.set_text(line)
            f.write(line.decode() + '\n')
        f.close()

    def config(self):

        if isCrypto:
            if self.loadFile or os.environ.get('appname',None) is None:
                self.decrypt_file('.env')
        else:
            self.load_file('.env')

        return os.environ
            

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--option', help='fazer uma das seguintes ações: [crypto, append, generate]')
    args = parser.parse_args()
    
    if args.option == 'generate':
        api_key = Fernet.generate_key()
        api_key = api_key.decode()
        print(f'Adicione as variaveis de ambiente API_KEY={api_key} e API_USER=<seu nome>')
    else:
        c = crypto_file()

        if args.option:
            if args.option == 'crypto':
                if os.path.isfile('.env.base'):
                    c.crypto_file('.env.base')
        
            if args.option == 'append':
                if os.path.isfile('.env.append'):
                    c.append_line('.env.append')