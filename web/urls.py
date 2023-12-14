from django.urls import path
from web import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='registration'),
]
