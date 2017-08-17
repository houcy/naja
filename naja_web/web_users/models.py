from django.db import models
from django.core.validators import MaxValueValidator


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
    class Meta:
        db_table = 'Bugs'  # 数据表名称


class Plugin(models.Model):
    name = models.CharField(max_length=256)
    type_type = (
        ('COM', '通用插件'),
        ('POC', '漏洞探测插件'),
        ('EXP', '漏洞利用插件'),
    )
    type = models.CharField(max_length=3, choices=type_type)
    risk_type = (
        ('H', '高危'), # 代码执行
        ('M', '中危'), # 写权限 数据库 内存 文件系统
        ('L', '低危'), # 读取服务器上的信息 数据库 内存 文件系统  DDOS
        ('I', '信息'), # 端口扫描 指纹识别
    )
    risk = models.CharField(max_length=4, choices=risk_type)

    '''
    grade_type = (
        (0, 'target'),      # 00000001      target_common target_google target_zoomeye target_shodan
        (1, 'Host'),        # 00000001      nmap
        (2, 'Port'),        # 00000010
        (4, 'Proto'),       # 00000100      ms17-010
        (8, 'Service'),     # 00001000      spider
        (16, 'SBanner'),    # 00010000      WFTP-RCE
        (32, 'URL'),        # 00100000      SQL注入
        (64, 'UBanner'),    # 01000000      S-020 Jeklins-SQL
    )
    grade = models.PositiveSmallIntegerField(default=1, choices=grade_type)
    '''
    usage = models.TextField()
    description = models.TextField()
    exec_path = models.CharField(max_length=256)

    class Meta:
        db_table = 'Plugin'  # 数据表名称

    def __str__(self):
        # 用于Forms显示外键内容
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=256)
    targets = models.TextField()
    count = models.IntegerField(default=-1)
    timestamp = models.TimeField(auto_now_add=True)
    status_type = (
        ('S', '扫描中'),
        ('F', '已完成'),
        ('E', '异常终止'),
    )
    #bug_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1, choices=status_type)
    plugin = models.ManyToManyField(Plugin)

    class Meta:
        db_table = 'Task'  # 数据表名称
