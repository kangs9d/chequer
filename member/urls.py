from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add/$', views.add, name='add'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^get/$', views.get, name='get'),
    url(r'^list/$', views.list_member, name='list'),
]
