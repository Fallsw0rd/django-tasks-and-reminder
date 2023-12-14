from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskList(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название задачи')
    description = models.TextField(verbose_name='Описание')
    due_date = models.DateField(verbose_name='Срок выполнения')
    priority = models.IntegerField(verbose_name='Приоритет')
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def has_reminders(self):
        return self.reminder_set.exists()


class Reminder(models.Model):
    reminder_datetime = models.DateTimeField(verbose_name='Дата напоминания')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return f"Напоминание для {self.task.title} ({self.reminder_datetime})"