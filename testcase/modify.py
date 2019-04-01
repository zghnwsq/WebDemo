# coding:utf8

from django import forms


class ModifyForm(forms.Form):
    no = forms.CharField(max_length=20, strip=True, required=False)
    case = forms.CharField(max_length=50, strip=True, required=False)
    project = forms.Select()
    path = forms.FileInput()
    sheet = forms.CharField(max_length=32)


