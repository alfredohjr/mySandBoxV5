from email.mime import base
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from jobs.core.api.viewsets import ScriptsViewSets, ExecutionManualViewSets, ExecutionLogViewSets

router = routers.DefaultRouter()
router.register('api/scripts', ScriptsViewSets, basename='jobsscripts')
router.register('api/manual', ExecutionManualViewSets, basename='jobsmanual')
router.register('api/log', ExecutionLogViewSets, basename='executionlog')

urlpatterns = [
    path('',include(router.urls)),
]