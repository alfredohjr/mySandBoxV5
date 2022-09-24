from rest_framework import serializers
from jobs.models import Scripts, ExecutionManual, ExecutionLog
from django.db.models import F, Avg

class ScriptsSerializer(serializers.ModelSerializer):

    executionTimeAvgSeconds = serializers.SerializerMethodField()    

    def get_executionTimeAvgSeconds(self,obj):
        queryset = ExecutionLog.objects.filter(script_id=obj.id)
        queryset = queryset.values('script_id').annotate(time=Avg(F('finishedAt') - F('startedAt')))
        if queryset:
            return queryset[0]['time']

    class Meta:
        model = Scripts
        fields = '__all__'


class ExecutionManualSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExecutionManual
        fields = '__all__'


class ExecutionLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExecutionLog
        fields = '__all__'
