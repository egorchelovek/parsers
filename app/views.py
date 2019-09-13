from django.shortcuts import render
from app.models import Worker

# Create your views here.
def workers_list(request):
    workers = Worker.objects.all();
    return render(request, "app/workers_list.html", {'workers':workers})
