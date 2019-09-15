from django.urls import path
from . import views

urlpatterns = [
    path('',views.workers_list, name='workers_list'),
    path('worker/new/', views.worker_new, name='worker_edit'),
    path('worker/<int:pk>/edit/', views.worker_edit, name='worker_edit'),
    path('worker/<int:pk>/delete/', views.worker_delete, name='worker_delete'),
    path('worker/<int:pk>/activate/', views.worker_activate, name='worker_activate'),
    path('worker/<int:pk>/stop/', views.worker_stop, name='worker_stop'),
]
