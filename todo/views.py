from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Task
from .forms import TaskForm
import json

def task_list(request):
    tasks = Task.objects.all().order_by('id')
    form = TaskForm()
    return render(request, 'todo/task_list.html', {'tasks': tasks, 'form': form})  # ← 修正ポイント！

@require_POST
def add_task(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect('task_list')

@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

@require_POST
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')

@require_POST
def reorder_tasks(request):
    data = json.loads(request.body)
    ids = data.get('task_ids', [])
    for i, task_id in enumerate(ids):
        task = Task.objects.get(id=task_id)
        task.order = i
        task.save()
    return JsonResponse({'success': True})

@require_POST
def update_task(request, task_id):
    try:
        data = json.loads(request.body)
        title = data.get("title", "").strip()
        due_date = data.get("due_date", None)

        if not title:
            return JsonResponse({"error": "タイトルは必須です"}, status=400)

        task = Task.objects.get(pk=task_id)
        task.title = title
        task.due_date = due_date if due_date else None
        task.save()
        return JsonResponse({"success": True})
    except Task.DoesNotExist:
        return JsonResponse({"error": "タスクが見つかりません"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
