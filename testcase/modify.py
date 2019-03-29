# coding:utf8

from django import forms

class ModifyForm(forms.Form):
    no = forms.CharField(max_length=20)
    case = forms.CharField(max_length=50)
    project = forms.Select()
    path = forms.FileInput()
    case = forms.CharField(max_length=32)


