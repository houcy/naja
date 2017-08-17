from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.urls import reverse

from django.views.generic import CreateView, DeleteView, UpdateView, ListView, DetailView

from . import models


# 查询列表
class MyListView(ListView):
    # 读取所有数据记录
    def get_queryset(self):
        return self.model.objects.all()

# 查询详细信息
class MyDetailView(DetailView):
    # 查询当前数据记录
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

# 增
class MyCreateView(CreateView):
    def get_success_url(self):
        return reverse(self.success_url, args=(str(self.object.pk), ))

# 删
class MyDeleteView(DeleteView):
    def get_object(self, queryset=None):
        return super(MyDeleteView, self).get_object()

# 改
class MyUpdateView(UpdateView):
    # 查询当前数据记录
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['pk'])

    # 自定义success_url
    def get_success_url(self):
        return reverse(self.success_url, args=(str(self.kwargs['pk']), ))



class BugsList(ListView):
    model = models.Bugs
    template_name = 'bug_list.html'

class PluginList(ListView):
    model = models.Plugin
    template_name = 'bug_list.html'


def task_list(request):
    return render(request, "task_list.html")
    #return HttpResponse("Hello, naja web users.")

def task_details(request):
    return render(request, "task_details.html")

def task_create(request):
    return render(request, "task_create.html")

def bug_list(request):
    return render(request, "bug_list.html")


def home(request):
    return render(request, "home.html")
