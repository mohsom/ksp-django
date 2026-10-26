from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TaskForm
from .models import Task


def task_list(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_list.html', {'tasks': Task.objects.all(), 'form': form})


@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    task.save()
    return redirect('task_list')


@require_POST
def task_delete(request, pk):
    get_object_or_404(Task, pk=pk).delete()
    return redirect('task_list')
