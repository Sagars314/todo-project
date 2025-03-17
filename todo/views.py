from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all().order_by('due_date', 'priority') # Default: show all tasks

    # Get filter parameters from the request
    filter_type = request.GET.get('filter', 'all')  # Default: 'all'
    priority_filter = request.GET.get('priority', 'all')  # Default: 'all'

    # Apply filters based on user selection
    if filter_type == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_type == 'pending':
        tasks = tasks.filter(completed=False)

    if priority_filter in ['High', 'Medium', 'Low']:
        tasks = tasks.filter(priority=priority_filter)


    form = TaskForm()
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')

    return render(request, 'todo/task_list.html', {
        'tasks': tasks, 
        'form': form,
        'filter_type': filter_type,
        'priority_filter': priority_filter,
        })

def task_complete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')

def task_delete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')
