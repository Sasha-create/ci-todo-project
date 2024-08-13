from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from .models import Task

class CustomLoginView(LoginView):
    template_name = 'student_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'student_app/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    modal = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDetail(LoginRequiredMixin, DetailView):
    template_name = 'student_app/task_detail.html'
    context_object_name = 'task'
    modal = Task
    
    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['pk'], user=self.request.user)

class TaskCreate(LoginRequiredMixin, CreateView):
    modal = Task
    template_name = 'student_app/task_form.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task successfully added!")
        return super(TaskCreate, self).form_valid(form)
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    modal = Task
    template_name = 'student_app/task_form.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class TaskDelete(LoginRequiredMixin, DeleteView):
    modal = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Task successfully deleted!")
        return super(TaskDelete, self).delete(request, *args, **kwargs)