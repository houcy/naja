from django.db import models

class Bugs(models.Model):
    country = models.CharField(max_length=256)
    host = models.CharField(max_length=256)
    bug_name = models.CharField(max_length=256)
    bug_class = models.CharField(max_length=256)
    road = models.CharField(max_length=256)
    last_time = models.CharField(max_length=256)
    usable = models.CharField(max_length=256)
    information = models.CharField(max_length=65535)
    author = models.CharField(max_length=256)

class Plugin(models.Model):
    name = models.CharField(max_length=256)
    cve = models.CharField(max_length=256)
    rank = models.CharField(max_length=256)
    python = models.CharField(max_length=256)
    usage = models.CharField(max_length=256)
    result = models.CharField(max_length=256)


class Task(models.Model):
    name = models.CharField(max_length=256)
    cve = models.CharField(max_length=256)
    rank = models.CharField(max_length=256)
    python = models.CharField(max_length=256)
    usage = models.CharField(max_length=256)
    result = models.CharField(max_length=256)