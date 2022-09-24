from rest_framework import viewsets
from jobs.models import ExecutionLog, Scripts, ExecutionManual
from jobs.core.api.serializers import ScriptsSerializer, ExecutionManualSerializer, ExecutionLogSerializer

class ScriptsViewSets(viewsets.ReadOnlyModelViewSet):

    serializer_class = ScriptsSerializer

    def get_queryset(self):
        queryset = Scripts.objects.all()
        queryset = queryset.filter(active=True)

        return queryset


class ExecutionManualViewSets(viewsets.ModelViewSet):

    serializer_class = ExecutionManualSerializer

    def get_queryset(self):
        queryset = ExecutionManual.objects.all()

        return queryset


class ExecutionLogViewSets(viewsets.ReadOnlyModelViewSet):

    serializer_class = ExecutionLogSerializer

    def get_queryset(self):
        queryset = ExecutionLog.objects.all()
        return queryset