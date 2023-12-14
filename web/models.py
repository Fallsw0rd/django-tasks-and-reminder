from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class TaskList(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.IntegerField()
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE)


class Reminder(models.Model):
    reminder_datetime = models.DateTimeField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Rating(models.Model):
    rating_value = models.IntegerField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
