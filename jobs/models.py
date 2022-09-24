from django.db import models
from django.utils import timezone

# Create your models here.

class Groups(models.Model):

    name = models.CharField(max_length=30)
    active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.name


class Scripts(models.Model):

    name = models.CharField(max_length=50)
    description = models.TextField()
    script = models.TextField()
    group = models.ForeignKey(Groups,on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Crontab(models.Model):

    name = models.CharField(max_length=50)
    script = models.ForeignKey(Scripts,on_delete=models.CASCADE)
    description = models.TextField()
    active = models.BooleanField(default=False)
    minute = models.CharField(max_length=20)
    hour = models.CharField(max_length=20)
    dayOfMonth = models.CharField(max_length=20)
    month = models.CharField(max_length=20)
    dayOfWeek = models.CharField(max_length=20)
    arguments = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ExecutionLog(models.Model):

    script = models.ForeignKey(Scripts, on_delete=models.CASCADE)
    crontab = models.ForeignKey(Crontab, on_delete=models.CASCADE,null=True,blank=True)
    startedAt = models.DateTimeField(null=True, blank=True)
    finishedAt = models.DateTimeField(null=True, blank=True)
    success = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)


class ExecutionManual(models.Model):

    script = models.ForeignKey(Scripts,on_delete=models.CASCADE)
    user = models.IntegerField(default=0)
    run = models.BooleanField(default=True)
    arguments = models.TextField(blank=True, null=True)
    startAt = models.DateTimeField(default=timezone.now)
    finishedAt = models.DateTimeField(blank=True, null=True)


