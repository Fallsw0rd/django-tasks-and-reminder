from django.urls import path
from web import views

urlpatterns = [
    # main page
    path('', views.index_view, name='index'),

    # auth
    path('register/', views.register_view, name='registration'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # task_list
    path('task_lists/add/', views.edit_task_list, name='add_task_list'),
    path('task_lists/<int:id>/edit/', views.edit_task_list, name='edit_task_list'),

    # task
    path('task_lists/<int:ts_id>/tasks/', views.list_tasks, name='list_tasks'),
    path('task_lists/<int:ts_id>/tasks/add/', views.edit_task, name='add_task'),
    path('task_lists/<int:ts_id>/tasks/<int:cur_task>/edit/', views.edit_task, name='edit_task'),
    path('task_lists/<int:ts_id>/tasks/<int:cur_task>/delete/', views.delete_task, name='delete_task'),

    # reminder
    path('tasks/<int:task_id>/reminders/', views.list_reminders, name='list_reminders'),
    path('tasks/<int:task_id>/reminders/add/', views.edit_reminder, name='add_reminder'),
    path('tasks/<int:task_id>/reminders/<int:cur_reminder>/edit/', views.edit_reminder, name='edit_reminder'),
    path('tasks/<int:task_id>/reminders/<int:cur_reminder>/delete/', views.delete_reminder, name='delete_reminder'),

    # analytics
    path('analytics/', views.analytics_view, name='analytics'),
]
