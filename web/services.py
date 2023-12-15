import csv
import io
from datetime import datetime

from web.models import Task, TaskList


def filter_tasks(tasks_qs, filters: dict):
    if filters['search']:
        tasks_qs = tasks_qs.filter(title__icontains=filters['search'])

    if filters['priority'] != '':
        tasks_qs = tasks_qs.filter(priority=filters['priority'])

    if filters['choose_date']:
        tasks_qs = tasks_qs.filter(due_date=filters['choose_date'])
    return tasks_qs


def export_tasks_csv(tasks_qs, response):
    writer = csv.writer(response)
    writer.writerow(('title', 'description', 'due_date', 'priority', 'task_list'))

    for task in tasks_qs:
        writer.writerow((
            task.title, task.description, task.due_date, task.priority, task.task_list.name
        ))

    return response


def import_tasks_from_csv(file):
    file_content = file.read().decode('utf-8')

    csv_file = io.StringIO(file_content)

    csv_reader = csv.reader(csv_file)
    next(csv_reader)

    for row in csv_reader:
        title, description, due_date_str, priority_str, task_list_name = row
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        priority = int(priority_str)
        task_list, created = TaskList.objects.get_or_create(name=task_list_name)

        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            task_list=task_list
        )
