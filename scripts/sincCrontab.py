from jobs.models import Scripts, Crontab

def run():
    f = open('tmp/crontab.tab','r')
    l = f.readlines()
    f.close()

    nl = []
    for i in l:
        if not i.startswith(('#','\n')):
            nl.append(i.replace('\n',''))

    for i in nl:
        i = i.split()
        minute = i[0]
        hour = i[1]
        dayOfMonth = i[2] 
        month = i[3]
        dayOfWeek = i[4]
        script = ' '.join(i[5:])
        
        s = Scripts(name=f'[Definir] - {script[0:15]}'
                    , description=f'[Definir] - {script}'
                    , script=script
                    , active = False)
        s.save()

        c = Crontab(name=f'[Definir] - {script[0:15]}'
                    , script = s
                    , description = f'[Definir] - {script}'
                    , active = False
                    , minute = minute
                    , hour = hour
                    , dayOfMonth = dayOfMonth
                    , month = month
                    , dayOfWeek = dayOfWeek)
        c.save()