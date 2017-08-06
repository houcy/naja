from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse


from django.views.generic.detail import DetailView

from django.views.generic.list import ListView

from . import models

class BugsList(ListView):
    model = models.Bugs
    template_name = 'bug_list.html'

class PluginList(ListView):
    model = models.Plugin
    template_name = 'bug_list.html'


def index(request):
    return render(request, "task_list.html")
    #return HttpResponse("Hello, naja web users.")

def task_details(request):
    return render(request, "task_details.html")

def task_create(request):
    return render(request, "task_create.html")


def bug_list(request):
    return render(request, "bug_list.html")


def test(request):
    return render(request, "index.html")
