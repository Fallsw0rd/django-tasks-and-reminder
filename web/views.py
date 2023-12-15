from datetime import datetime
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Max, Min, Q
from django.db.models.functions import TruncDate
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from web.forms import RegistrationForm, AuthForm, TaskListForm, TaskForm, ReminderForm, TaskFilterForm
from web.models import TaskList, Task, Reminder
from web.services import filter_tasks, export_tasks_csv

User = get_user_model()


def index_view(request):
    user = request.user
    if user.is_authenticated:
        task_lists = TaskList.objects.filter(user=user).select_related('user')
        page_number = request.GET.get('page', 1)
        paginator = Paginator(task_lists, per_page=5)
        return render(request, "web/main.html", {'tasklists': paginator.get_page(page_number)})
    else:
        return render(request, "web/main.html")


def register_view(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
            )
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)

            return redirect('index')

    return render(request, 'web/registration.html', {'form': form})


def login_view(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(data=request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is None:
                form.add_error(None, 'Введены неверные данные')
            else:
                login(request, user)

                return redirect('index')

    return render(request, 'web/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def edit_task_list(request, id=None):
    tasklist = get_object_or_404(TaskList, id=id) if id is not None else None
    form = TaskListForm(instance=tasklist)
    if request.method == 'POST':
        form = TaskListForm(request.POST, instance=tasklist)
        if form.is_valid():
            task_list = form.save(commit=False)
            task_list.user = request.user
            task_list.save()
            return redirect('index')

    return render(request, 'web/create_task_list.html', {'form': form})


@login_required
def delete_task_list(request, id=None):
    task_list = get_object_or_404(TaskList, id=id)
    task_list.delete()
    return redirect('index')


@login_required
def list_tasks(request, ts_id=None):
    today = datetime.now()
    task_list = get_object_or_404(TaskList, pk=ts_id)
    tasks = (Task.objects.filter(task_list=task_list, due_date__gte=today).order_by('due_date', '-priority')
             .select_related('task_list'))
    overdue_tasks = (Task.objects.filter(task_list=task_list, due_date__lt=today).order_by('due_date', '-priority')
                     .select_related('task_list'))
    reminder_task = Reminder.objects.filter(
        task_id__in=tasks.values_list('id'),
        reminder_datetime__time__lte=today,
        reminder_datetime__date__lte=today
    )

    filter_form = TaskFilterForm(request.GET)
    filter_form.is_valid()
    tasks = filter_tasks(tasks, filter_form.cleaned_data)

    total_count = tasks.count()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(tasks, per_page=5)

    if request.GET.get('export') == 'csv':
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=tasks.csv'}
        )
        return export_tasks_csv(tasks, response)

    return render(request, 'web/tasks.html', {'tasks': paginator.get_page(page_number),
                                              'overdue_tasks': overdue_tasks, 'total_count': total_count,
                                              'task_list': task_list, 'filter_form': filter_form,
                                              'today': today, 'reminder_task': reminder_task})


@login_required
def edit_task(request, ts_id=None, cur_task=None):
    task = get_object_or_404(Task, id=cur_task) if cur_task is not None else None
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.task_list_id = ts_id
            task.save()
            return redirect('list_tasks', ts_id=ts_id)

    return render(request, 'web/create_task.html', {'form': form})


@login_required
def delete_task(request, ts_id=None, cur_task=None):
    task = get_object_or_404(Task, id=cur_task)
    task.delete()
    return redirect('list_tasks', ts_id=ts_id)


@login_required
def list_reminders(request, task_id=None):
    task = get_object_or_404(Task, pk=task_id)
    reminders = Reminder.objects.filter(task=task)
    return render(request, 'web/reminders.html', {'reminders': reminders, 'task': task})


@login_required
def edit_reminder(request, task_id=None, cur_reminder=None):
    reminder = get_object_or_404(Reminder, id=cur_reminder) if cur_reminder is not None else None
    task = Task.objects.get(id=task_id)
    form = ReminderForm(instance=reminder)
    if request.method == 'POST':
        form = ReminderForm(request.POST, instance=reminder)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.task_id = task_id
            reminder.save()
            return redirect('list_reminders', task_id=task_id)

    return render(request, 'web/create_reminder.html', {'form': form, 'task': task})


@login_required
def delete_reminder(request, task_id=None, cur_reminder=None):
    reminder = get_object_or_404(Reminder, id=cur_reminder)
    reminder.delete()
    return redirect('list_reminders', task_id=task_id)


@login_required
def analytics_view(request):
    overall_stat = Task.objects.aggregate(
        Count('id'),
        Max('due_date'),
        Min('due_date'),
    )
    days_stat = (
        Task.objects.all()
        .annotate(date=TruncDate('due_date'))
        .values('date')
        .annotate(
            total_tasks=Count('id'),
            tasks_with_reminders=Count('id',filter=Q(reminder__isnull=False)))
    ).order_by('due_date')

    return render(request, 'web/analytics.html', {'overall_stat': overall_stat,
                                                  'days_stat': days_stat})
