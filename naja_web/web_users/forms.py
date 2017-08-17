from django import forms

from django.forms import widgets

from . import models

class MyCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = 'widgets/multiple_input.html'
    option_template_name = 'widgets/input_option.html'

class TaskForm(forms.ModelForm):

    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "任务名称"}),
    )

    targets = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': "目标列表"}),
    )

    plugin = forms.ModelMultipleChoiceField(
        # 外键的初始化
        queryset= models.Plugin.objects.all(),  # TODO 减少查询列
        # 自定义Widget样式 TODO:总结
        widget=MyCheckboxSelectMultiple(attrs={'sonclass': 'checkbox-inline', 'grandsonclass': 'label label-default'}),
    )
    class Meta:
        model = models.Task
        fields = ['name', 'targets', 'plugin']

class PluginForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "插件名称"}),
    )
    type = forms.ChoiceField(
        choices=models.Plugin.type_type,
        widget=forms.Select(attrs={'class': 'form-control', }),
    )
    risk = forms.ChoiceField(
        choices=models.Plugin.risk_type,
        widget=forms.Select(attrs={'class': 'form-control', }),
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': "插件描述"}),
    )
    usage = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': "使用方法"}),
    )
    exec_path = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "/plugins/*.py"}),
    )

    class Meta:
        model = models.Plugin
        fields = ['name', 'type', 'risk', 'description', 'usage', 'exec_path']