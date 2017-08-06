
from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^test/', views.test, name='test'),
    url(r'^task/', views.index, name='index'),
    url(r'^task_details/', views.task_details, name='task_details'),
    url(r'^task_create/', views.task_create, name='task_create'),
    url(r'^bug_list/$', views.PluginList.as_view()),
]