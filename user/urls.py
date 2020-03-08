from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^signup/$', views.sign_up, name='sign_up'),
    url(r'^signin/$', views.sign_in, name='sign_in'),
    url(r'^logout/$', views.log_out, name='logout'),
]
