import re
import requests
import datetime
import time
import os

token = str()
baseurl = str()
if os.getenv('fr_baseurl') and os.getenv('fr_token'):
    baseUrl = os.getenv('fr_baseurl')
    token = f'Token {os.getenv("fr_token")}'
else:
    print('Por favor confira as variaveis de ambiente fr_baseurl and fr_token')
    time.sleep(60)

header = {'Authorization':token}

response = requests.get(baseUrl + '/jobs/api/scripts/?limit=200', headers=header)

results = response.json().get('results')

for r in results:
    if r.get('active') == True:
        print(f'{r.get("id")} - {r.get("name")} || média({round(float(r.get("executionTimeAvgSeconds")),2)} segundo(s))')

print('Digite o ID da tarefa:')
inputId = input()

if inputId == 'test':

    for r in results:
        if r.get('active') == True:
            data = {
                'user': 1,
                'run': True,
                'startAt': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M-03:00'),
                'script': int(r.get("id"))
            }    
            response = requests.post(baseUrl + '/jobs/api/manual/', headers=header, json=data)
            print(f'{r.get("name")} enviado para a fila.')
            time.sleep(1)

else:
    data = {
        'user': 1,
        'run': True,
        'startAt': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M-03:00'),
        'script': int(inputId)
    }
    response = requests.post(baseUrl + '/jobs/api/manual/', headers=header, json=data)

    if response.status_code == 201:
        print('Adicionado na fila de execução')
    else:
        print('Erro ao adicionar na fila de execução')
        time.sleep(60)