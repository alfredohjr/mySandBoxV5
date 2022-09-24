from genericpath import isfile
import pandas as pd
import os

from jobs.models import Scripts

def run(*args):

    file = 'tmp/jobs_scripts.csv'
    if os.path.isfile(file):
        df = pd.read_csv(file)
        df = df[['name','description','script']]

        queryset = Scripts.objects.all()
        queryset.delete()

        for i,v in df.iterrows():
            s = Scripts(name=v['name'], description=v['description'], script=v['script'])
            s.save()
    else:
        print(f'arquivo {file} não encontrado')