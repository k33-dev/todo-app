import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.views.decorators.csrf import csrf_exempt

@login_required
def index(request):
    tasks = Task.objects.filter(user=request.user).order_by('order')
    form = TaskForm()
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'form': form})

@login_required
@require_POST
def add_task(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
    return redirect('index')

@login_required
@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return JsonResponse({'status': 'ok'})

@login_required
@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('index')

@login_required
@require_POST
@csrf_exempt
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    data = json.loads(request.body)
    task.title = data.get('title', task.title)
    task.due_date = data.get('due_date', task.due_date)
    task.save()
    return JsonResponse({'status': 'ok'})

@login_required
@require_POST
@csrf_exempt
def reorder_tasks(request):
    data = json.loads(request.body)
    task_ids = data.get('task_ids', [])
    for i, task_id in enumerate(task_ids):
        Task.objects.filter(id=task_id, user=request.user).update(order=i)
    return JsonResponse({'status': 'ok'})
