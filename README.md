# mySandBoxV5

Um aplicativo para automatizar rotinas utilizando python.

Homologado para Python 3.10.

![](https://github.com/alfredohjr/mySandBoxV5/raw/master/docs/media/logo.png#vitrinedev)

## Para instalar!

1. Faça o clone do repositório.
    ```console
    git clone https://github.com/alfredohjr/mySandBoxV5
    ```

1. Acesse o repositório.
    ```console
    cd mySandBoxV5
    ```

1. Crie o ambiente virtual.
    ```console
    python -m venv amb
    ```
    *Obs.: por enquanto sempre crie o ambiente amb dentro do projeto para que os processos funcionem de acordo.*

1. Ative o ambiente virtual.
    Windows:
    ```console

    amb\Scripts\activate.bat
    ```
    Linux:
    ```console
    source amb/lib/activate
    ```

1. Instale as dependências.
    ```console
    pip install -r requirements.txt
    ```

1. Copie o arquivo .env.example para .env
    ```console
    cp .env.example .env
    ```

1. Crie a SECRET_KEY [Aqui](https://djecrety.ir/).

1. Coloque a SECRET_KEY na chave SECRET_KEY no arquivo .env

1. execute as migrations.
    ```command
    python manage.py migrate
    ```

2. Iniciando o projeto:
    Web.
    ```console 
    python manage.py runserver
    ```
    Crontab.
    ```console
    python manage.py runscript runCrontab
    ```
## Detalhes:
1. O processo só lê os Scripts da pasta jobs/scripts

## Funcionalidades:
1. Crie crontabs de Scripts feito em python.
   1. Adicione o script.
    ![log](https://github.com/alfredohjr/mySandBoxV5/raw/master/docs/media/script.gif)
   1. Adicione o crontab crontab.
    ![log](https://github.com/alfredohjr/mySandBoxV5/raw/master/docs/media/crontab.gif)

    *Obs.: para o crontab, utilize as sintaxes \*(sempre), 1-5(de segunda a sexta), 1/10(a cada 10 minutos) ou 12(somente em dezembro).* 
2. Visualize log de execução.
    ![log](https://github.com/alfredohjr/mySandBoxV5/raw/master/docs/media/log.gif)
3. Agende tarefas para o futuro.
    ![log](https://github.com/alfredohjr/mySandBoxV5/raw/master/docs/media/manual.gif)

## Outras funcionalidades.
1. Mande mensagens.
   1. Telegram.
    ```python
    from jobs.core.main import f_send_msg

    f_send_msg(msg='teste',contato='id')
    ```
   
   2. Email.
    ```python
    from jobs.core.main import f_send_mail
    # sem anexo 
    f_send_mail(titulo='teste',mensagem='teste',para='teste@localhost')

    # com anexo 
    f_send_mail(titulo='teste',mensagem='teste',anexo='tmp/arquivo.pdf',para='teste@localhost')
    ```
    *Obs.: se o parametro para não for informado, a função vai tentar enviar para o contato da variavel admin_email, indicado no arquivo .env*


2. Formate arquivos em Excel.
    ```python
    import pandas as pd
    from jobs.core.main import df2Excel

    df = pd.DataFrame()
    arq = df2Excel(df,'tmp/out.xlsx')
    
    # Formata coluna para numero
    arq.toNumber(['A','C','D'])

    # Formata coluna para dinheiro
    arq.toCurrency(['A','C','D'])

    # Formata coluna para CPF
    arq.toCPF(['A','C','D'])

    # Formata coluna para CNPJ
    arq.toCNPJ(['A','C','D'])

    # Formata coluna para telefone
    arq.toTel(['A','C','D'])

    # Formata coluna para celular
    arq.toCel(['A','C','D'])

    # Formata coluna para porcentagem
    arq.toPercent(['A','C','D'])

    # Alinha os dados no centro da coluna
    arq.toAlignCenter(['A','C','D'])

    # salva o arquivo em disco
    arq.save()
    ```

3. Crie listas de datas.
    ```python
    from jobs.core.main import f_periodo_v6

    for data in f_periodo_v6(dias=90,fmt='%Y%m'):
        print(data)
    ```

4. Crie arquivos de log padronizado.
    ```python
    from jobs.core.main import setup_logger

    log = setup_logger('readme')
    log.info('Olá, estou funcionando')
    ```
    *Obs.: procure usar o log por aqui, o processo automaticamente compacta os arquivos antigos; os arquivos antigos estão disponiveis em tmp/log.*

5. Execute SQL.
    ```python
    from jobs.core.main import f_sqltodf, f_textodf

    # executando através de um arquivo sql.
    df = f_textodf('path/query.sql',banco='teste1')

    # executando sql diretamente.
    df = f_sqltodf('select * from dual',banco='teste1')
    ```
    *obs.: todos os comandos são salvos na pasta tmp/log; também é possível passar parametros extras através do arguments, para um dict com chave e valor; para o nome do banco utilize o nome dado na variavel bd_(nome) dentro do arquivo .env*

6. Execute funções no banco de dados(homologado somente para Oracle).
    Função usada para executar procedures no banco de dados oracle.
    
    Para parametros de saida utilize para NUMBER = cx_Oracle.NUMBER e VARCHAR = cx_Oracle.NCHAR.
    
    Para a variavel de entrada para_in utilize uma turple somente de
    caracteres.
    
    Para a variavel de entrada para_out faca o seguinte: crie variaveis
    para char ou number, depois de criadas coloque-as em uma lista e informe
    no paramentro.

    ```python
    banco = 'teste'
    procedure = 'PROC_TESTE'
    para_in = ['1','0','044064','0']
    
    var1 = '0'
    var2 = 0.
    para_out = [var1,var2]
    
    saida = f_execproc(banco = 'prdrac',para_in = para_in, para_out = para_out, procedure = procedure)    
    ```

7. Envie arquivos para o Google Drive.
    ```python
    import pandas as pd
    from jobs.core.main import Sheet, File

    df = pd.DataFrame()
    df.to_csv('tmp/exemplo.csv')

    # Enviando arquivo e já convertendo para o sheets do drive
    sheet = Sheet()
    sheet.create('tmp/exemplo.csv')
    # Atualizando arquivo no drive
    sheet.update('tmp/exemplo.csv')

    # Enviando arquivo para o drive, sem conversão.
    file = File()
    file.create('tmp/exemplo.csv')
    # Atualizando arquivo no drive
    file.create('tmp/exemplo.csv')
    ```

