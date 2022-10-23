from django.contrib import admin

from jobs.models import Crontab, ExecutionManual, Scripts, Groups, ExecutionLog
# Register your models here.

class ScriptAdmin(admin.ModelAdmin):

    list_display = ('name','description','active')
    list_filter = ['active']


class CrontabAdmin(admin.ModelAdmin):
    
    list_display = ('name','script','minute','hour','dayOfMonth','month','dayOfWeek','active')

class ManualAdmin(admin.ModelAdmin):

    list_display = ('script','run','startAt','finishedAt')

class LogAdmin(admin.ModelAdmin):

    list_display = ('script','crontab','success','startedAt','finishedAt','message')
    list_filter = ['success','script','crontab']
    
    def has_change_permission(self, request, obj=None) -> bool:
        return False

admin.site.register(Crontab, CrontabAdmin)
admin.site.register(Scripts, ScriptAdmin)
admin.site.register(ExecutionManual, ManualAdmin)
admin.site.register(Groups)
admin.site.register(ExecutionLog, LogAdmin)