
from django.conf.urls import url

from . import views
from . import forms
from . import models

urlpatterns = [
    url(r'^home/', views.home, name='home'),

    url(r'^plugin/list/', views.MyListView.as_view(
        template_name='plugin_list.html',
        model=models.Plugin,
        paginate_by=10,
    ), name='plugin_list'),

    url(r'^plugin/create/', views.MyCreateView.as_view(
        model=models.Plugin,
        template_name='plugin_create.html',
        form_class=forms.PluginForm,
        success_url='plugin_details',
    ), name='plugin_create'),

    url(r'^plugin/details/(?P<pk>\d+)', views.MyDetailView.as_view(
        template_name='plugin_details.html',
        model=models.Plugin,
    ), name='plugin_details'),


    url(r'^task/create/', views.MyCreateView.as_view(
        template_name='task_create.html',
        form_class=forms.TaskForm,
        success_url='task_details',
    ), name='task_create'),

    url(r'^task/details/(?P<pk>\d+)', views.MyDetailView.as_view(
        template_name='task_details.html',
        model=models.Task,
    ), name='task_details'),

    url(r'^task/list/', views.MyListView.as_view(
        template_name='task_list.html',
        model=models.Task,
        paginate_by=10,
    ), name='task_list'),







    url(r'^task/list/', views.task_list, name='task_list'),
    url(r'^task/details/', views.task_details, name='task_details'),
    url(r'^bug/list/$', views.PluginList.as_view(), name='bug_list'),


]

'''





    # 列表
    url(r'^targets/list/', MyListView.as_view(
        template_name='targets_list.html',
        model=Targets,
        paginate_by=15
    ), name='targets_list'),
    # 详细信息
    url(r'^targets/details/(?P<pk>\d+)', login_required(MyDetailView.as_view(
        template_name='targets_details.html',
        model=Targets,
    )), name='targets_details'),
    # 创建
    url(r'^targets/create/', login_required(MyCreateView.as_view(
        template_name='targets_create.html',
        form_class=TargetsForm,
        success_url='targets_details',
    )), name='targets_create'),
    # 更新
    url(r'^targets/update/(?P<pk>\d+)', login_required(MyUpdateView.as_view(
        template_name='targets_update.html',
        form_class=TargetsForm,
        model=Targets,
        success_url='targets_details',
    )), name='targets_update'),
    # 删除
    url(r'^targets/delete/(?P<pk>\d+)', login_required(MyDeleteView.as_view(
        template_name = 'targets_delete.html',
        model=Targets,
        success_url = reverse_lazy('targets_list')
    )), name='targets_delete'),

'''