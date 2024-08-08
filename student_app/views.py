from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task

class TaskList(ListView):
    
    #modal = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDetail(DetailView):
    template_name = 'student_app/task_detail.html'
    context_object_name = 'task'
    #modal = Task
    
    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['pk'], user=self.request.user)

class TaskCreate(CreateView):
    modal = Task
    template_name = 'student_app/task_form.html'
    fields = '__all__'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskUpdate(UpdateView):
    modal = Task
    template_name = 'student_app/task_form.html'
    fields = '__all__'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDelete(DeleteView):
    modal = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)