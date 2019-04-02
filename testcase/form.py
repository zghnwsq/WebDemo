# coding:utf8

from django import forms
from django.forms import widgets
# from projects.models import ProjectsUser, Projects


class ModifyForm(forms.Form):
    no = forms.CharField(max_length=20, strip=True, required=False)
    case = forms.CharField(max_length=50, strip=True, required=False)
    # project = forms.Select()
    path = forms.FilePathField(path='', widget=widgets.FileInput, allow_folders=False, required=False)
    sheet = forms.CharField(max_length=32, required=False)


class NewForm(forms.Form):
    no = forms.CharField(max_length=20, strip=True, required=True)
    case = forms.CharField(max_length=50, strip=True, required=True)
    # project = forms.ChoiceField(widget=widgets.Select, required=True)
    # project = forms.Select()
    # path = forms.FileInput()
    path = forms.FilePathField(path='', widget=widgets.FileInput, allow_folders=False, required=False)
    sheet = forms.CharField(max_length=32, required=False)


