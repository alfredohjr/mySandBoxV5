import pandas as pd
import os

from jobs.models import Scripts, Crontab

def run(*args):

    file_script = 'tmp/jobs_scripts.csv'
    if not os.path.isfile(file_script):
        raise Exception('Arquivo de scripts não encontrado')
    
    df_scripts = pd.read_csv(file_script)

    file = 'tmp/jobs_crontab.csv'
    if os.path.isfile(file):
        df = pd.read_csv(file)

        queryset = Crontab.objects.all()
        queryset.delete()

        for i,v in df.iterrows():
            script_id = v['script_id']
            tmp_df = df_scripts.query(f'id == {script_id}')
            script_name = tmp_df['name'].values[0]
            queryset_script = Scripts.objects.filter(name=script_name)
            if queryset_script:
                script_id_new = queryset_script[0].id
                name = v['name']
                description = v['description']
                hour = v['hour']
                minute = v['minute']
                dayOfMonth = v['dayOfMonth']
                month = v['month']
                dayOfWeek = v['dayOfWeek']
                arguments = v['arguments']
                
                c = Crontab(name=name
                            , description=description
                            , script_id=script_id_new
                            , hour=hour
                            , minute = minute
                            , dayOfMonth = dayOfMonth
                            , month = month
                            , dayOfWeek = dayOfWeek
                            , arguments = arguments)
                c.save()
            else:
                print(f'script "{script_name}" não encontrado.')
    else:
        print(f'arquivo {file} não encontrado')