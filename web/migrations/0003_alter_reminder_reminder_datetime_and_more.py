# Generated by Django 5.0 on 2023-12-14 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_delete_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminder',
            name='reminder_datetime',
            field=models.DateTimeField(verbose_name='Дата напоминания'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='task',
            name='due_date',
            field=models.DateField(verbose_name='Срок выполнения'),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(verbose_name='Приоритет'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название задачи'),
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]