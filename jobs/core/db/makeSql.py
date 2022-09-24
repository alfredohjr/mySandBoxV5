import json
import os

class DbMain:
    
    def __init__(self,sistema:str,tabela:str,data:list):
        self._tabela = tabela
        self._data = data
        self._arquivo = f'jobs/core/db/_meta/{sistema}/{tabela}.json'
        
        if os.path.isfile(self._arquivo):
            f = open(self._arquivo,'r')
            f1 = f.readlines()
            f.close()
            
            f1 = ' '.join([x.replace('\n',' ') for x in f1])
            
            self._meta = json.loads(f1)
        else:
            print(f'arquivo {self._arquivo} não encontrado')
    
    def insert(self):
        tabela = self._tabela
        c = list()
        V = list()
        for k,v in self._meta['meta'].items():
            c.append(v['db_table'])
            
            if k in self._data:
                tmp_v = self._data[k]
                if type(tmp_v) == float:
                    V.append(f"{tmp_v}")
                else:
                    V.append(f"'{tmp_v}'")
            else:
                try:
                    V.append(f"'{v['padrao']}'")
                except:
                    print(k)
        
        textInsert = f'''insert into {tabela}({", ".join([str(x) for x in c])}) values({",".join([str(x) for x in V])})'''
        return textInsert
        
    def columns(self):
        
        nl = list()
        for k, v in self._meta['meta'].items():
            if 'padrao' in v:
                pass
            else:
                nl.append(k)
        return nl


class dbGenerateMeta:
    
    def __init__(self,df,sistema,tabela):
        self._df = df
        self._sistema = sistema
        self._tabela = tabela
        self._file = f'jobs/core/db/_meta/{self._sistema}/{self._tabela}.json'
    
    def create(self):
        if os.path.isfile(self._file):
            return 0
        
        f = open(self._file,'w')
        f.write('{\n')
        f.write('"meta": {')
        nl = list()
        for k in df.keys():
            v = df[k].values[0]
            nl.append('\t\t"' + k + '":{"tipo":"int","db_table":"' + k + '","padrao":"' + str(v) + '"}')
        
        f.write('\n')
        f.write(', \n'.join(nl))
        f.write('\n\t}\n}')
        f.close()