from django.urls import path
from . import views

urlpatterns = [
    path('',views.workers_list, name='workers_list'),
    path('worker/<int:pk>/edit/', views.worker_edit, name='worker_edit'),
    path('worker/new/', views.worker_new, name='worker_edit'),
]
