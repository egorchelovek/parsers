from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from app.models import Worker
from app.forms import WorkerForm
import json
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery.result import AsyncResult

def create_new_task(worker):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=worker.updating_period,
        period=IntervalSchedule.SECONDS,
    )

    task_name = 'task'+str(worker.id)
    task = PeriodicTask.objects.create(
        interval=schedule,
        name=task_name,
        task='app.tasks.parse_and_report',
        args=json.dumps([worker.id]),
    )
    return task


@login_required
def task_update(request, task_id):
    # if pk != 0:
    #     task = AsyncResult(str(pk))
    #     progress = 0
    #     # if hasattr(task.info, 'progress'):
    #     #     progress = task.info['progress']
    #     data = {
    #         'state': task.state,
    #         'progress': progress
    #     }
    # else:
    result = AsyncResult(task_id)
    print("TASK_ID {}".format(task_id))
    print(result.state)
    data = {
        'state':'void',
        'progress':'0'
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

@login_required
def monitor(request):
    workers = Worker.objects.all()
    return render(request, "app/monitor.html", {'workers':workers})
#
# @login_required
# def list_of_workers():
#     return

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
    if worker.task_id != 0:
        try:
            task = PeriodicTask.objects.get(pk=worker.task_id)
            task.delete()
        except PeriodicTask.DoesNotExist:
            pass
    worker.delete()
    return redirect("/")

@login_required
def worker_activate(request, pk):

    worker = get_object_or_404(Worker, pk=pk)

    if worker.state_active == False:

        task = (create_new_task(worker) if worker.task_id == 0 else PeriodicTask.objects.get(pk=worker.task_id))

        task.enabled = True
        task.save()

        worker.task_id = task.id
        worker.state_active = True
        worker.save()

    return redirect("/")

@login_required
def worker_stop(request, pk):
    worker = get_object_or_404(Worker, pk=pk)

    if worker.state_active == True:

        task = PeriodicTask.objects.get(pk=worker.task_id)
        task.enabled = False
        task.save()

        worker.state_active = False
        worker.save()

    return redirect("/")
