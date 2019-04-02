from django import forms
# from django.forms import widgets

class ModifyForm(forms.Form):
    project = forms.CharField(max_length=32, strip=True, required=False)
    status = forms.CharField(max_length=8, strip=True, required=False)