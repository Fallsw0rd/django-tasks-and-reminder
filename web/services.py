import csv


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

