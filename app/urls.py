from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('',views.monitor, name='monitor'),
    url(r'^(?P<task_id>[\w-]+)/$', views.task_update, name='task_update'),
    path('worker/new/', views.worker_new, name='worker_edit'),
    path('worker/<int:pk>/edit/', views.worker_edit, name='worker_edit'),
    path('worker/<int:pk>/delete/', views.worker_delete, name='worker_delete'),
    path('worker/<int:pk>/activate/', views.worker_activate, name='worker_activate'),
    path('worker/<int:pk>/stop/', views.worker_stop, name='worker_stop'),
]
