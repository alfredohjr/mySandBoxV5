from django.contrib import admin

from jobs.models import Crontab, ExecutionManual, Scripts, Groups
# Register your models here.

class ScriptAdmin(admin.ModelAdmin):

    list_display = ('name','description','active')
    list_filter = ['active']


class CrontabAdmin(admin.ModelAdmin):
    
    list_display = ('name','script','minute','hour','dayOfMonth','month','dayOfWeek','active')


admin.site.register(Crontab, CrontabAdmin)
admin.site.register(Scripts, ScriptAdmin)
admin.site.register(ExecutionManual)
admin.site.register(Groups)