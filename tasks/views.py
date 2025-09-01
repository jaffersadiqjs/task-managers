from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from .forms import TaskForm
from django.utils.decorators import method_decorator

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Task List (with filtering)
@method_decorator(login_required, name='dispatch')
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        due_date = self.request.GET.get('due_date')
        if due_date:
            queryset = queryset.filter(due_date=due_date)
        return queryset

@method_decorator(login_required, name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

@method_decorator(login_required, name='dispatch')
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task created successfully.")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully.")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Task deleted successfully.")
        return super().delete(request, *args, **kwargs)
