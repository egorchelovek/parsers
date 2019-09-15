from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from app.models import Worker
from app.forms import WorkerForm
from app.task import parse_and_report

# Create your views here.
@login_required
def workers_list(request):
    workers = Worker.objects.all();
    return render(request, "app/workers_list.html", {'workers':workers})

@login_required
def worker_new(request):
    if request.method == "POST":
        form = WorkerForm(request.POST)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.creator = request.user
            worker.created_date = timezone.now()
            worker.save()
            return redirect('/')
    else:
        form = WorkerForm()
    return render(request, 'app/worker_edit.html',{'form':form})

@login_required
def worker_edit(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    if request.method == "POST":
        form = WorkerForm(request.POST, instance=worker)
        if form.is_valid():
            worker = form.save(commit=False)
            worker.creator = request.user
            worker.created_date = timezone.now()
            worker.save()
            return redirect('/')
    else:
        form = WorkerForm(instance=worker)
    return render(request, 'app/worker_edit.html',{'form':form})

@login_required
def worker_delete(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    worker.delete()
    return redirect("/")

@login_required
def worker_activate(request, pk):
    worker = get_object_or_404(Worker, pk=pk)
    parse_and_report(
    worker.email,
    worker.source,
    worker.objects_type,
    worker.objects_amount,
    worker.min_cost,
    worker.max_cost)
    return redirect("/")
