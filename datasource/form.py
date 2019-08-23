# coding:utf8

from django import forms
from django.forms import widgets


class ModifyForm(forms.Form):
    no = forms.CharField(max_length=20, strip=True, required=False)
    datasource = forms.CharField(max_length=50, strip=True, required=False)
    path = forms.FilePathField(path='.', widget=widgets.FileInput, allow_folders=False, required=False)  # path 2019.8.6
    sheet = forms.CharField(max_length=32, required=False)


class NewForm(forms.Form):
    no = forms.CharField(max_length=20, strip=True, required=True)
    datasource = forms.CharField(max_length=50, strip=True, required=True)
    path = forms.FilePathField(path='.', widget=widgets.FileInput, allow_folders=False, required=False)  # path 2019.8.6
    sheet = forms.CharField(max_length=32, required=False)