from django.shortcuts import render, HttpResponse
from django.utils import timezone

from jobs.models import Crontab, Scripts, ExecutionManual

# Create your views here.

def Crontab2Manual(request):

    scripts = Scripts.objects.filter(active=True)
    crontabs = Crontab.objects.filter(script__in=scripts, active=True)

    count = 0
    for crontab in crontabs:

        manual = ExecutionManual()
        manual.script = crontab.script
        manual.user = 1
        manual.run = 1
        manual.arguments = crontab.arguments
        
        startAt = timezone.datetime.now() + timezone.timedelta(minutes=count+(60*3))
        manual.startAt = startAt

        manual.save()

        count += 1

    return HttpResponse('<h1>Deu certo!</h1>')