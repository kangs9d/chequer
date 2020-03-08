from django.urls import path
from . import views

urlpatterns = [
    path('insert', views.insert, name='generate'),
    path('update', views.update, name='update'),
    path('index', views.index, name='index'),
    path('main', views.main, name='main'),
]