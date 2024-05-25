from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('importdata/', views.import_data, name="import_data"),
    path('exportdata/', views.export_data, name="export_data"),
    path('celerytest/', views.celery_test, name="celery_test"),
]
