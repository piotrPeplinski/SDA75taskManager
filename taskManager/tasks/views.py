from django.shortcuts import render
from .models import Task
from .forms import TaskForm
# Create your views here.


def home(request):
    return render(request, 'home.html')


def tasks(request):
    current = Task.objects.filter(
        user=request.user, complete_date__isnull=True)
    completed = Task.objects.filter(
        user=request.user, complete_date__isnull=False)
    return render(request, 'tasks.html', {'current': current, 'completed': completed})


def create(request):
    return render(request, 'create.html', {'form': TaskForm()})
