from django import forms
from django.contrib.auth import get_user_model

from web.models import TaskList, Task, Reminder

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error('password2', 'Пароли не совпадают')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class TaskListForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['name']


class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [
        (1, '1 - Низкий'),
        (2, '2 - Ниже среднего'),
        (3, '3 - Средний'),
        (4, '4 - Выше среднего'),
        (5, '5 - Высокий'),
    ]

    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority']
        widgets = {
            "due_date": forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d')
        }


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['reminder_datetime']
        widgets = {
            "reminder_datetime": forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M')
        }
