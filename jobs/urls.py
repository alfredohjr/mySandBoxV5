from email.mime import base
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from jobs.core.api.viewsets import ScriptsViewSets, ExecutionManualViewSets, ExecutionLogViewSets
from jobs.views import Crontab2Manual

router = routers.DefaultRouter()
router.register('/scripts', ScriptsViewSets, basename='jobsscripts')
router.register('/manual', ExecutionManualViewSets, basename='jobsmanual')
router.register('/log', ExecutionLogViewSets, basename='executionlog')

urlpatterns = [
    path('api',include(router.urls)),
    path('crontab2manual',Crontab2Manual,name='crontab2manual')
]