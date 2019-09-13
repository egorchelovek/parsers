from django.urls import path
from . import views

urlpatterns = [
    path('',views.workers_list, name='workers_list'),
]
