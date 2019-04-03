from django import forms
# from django.forms import widgets

class ModifyForm(forms.Form):
    no = forms.CharField(max_length=20, strip=True, required=False)
    name = forms.CharField(max_length=50, strip=True, required=False)
    # project select disabled
    # case select
    # ds select
    ip = forms.GenericIPAddressField(strip=True, required=False)
    ds_range = forms.CharField(max_length=72, strip=True, required=False)


class NewForm(forms.Form):
    no = forms.CharField(max_length=20, strip=True, required=True)
    name = forms.CharField(max_length=50, strip=True, required=True)
    # project select required=True
    # case select  required=False
    # ds select required=False
    ip = forms.GenericIPAddressField(strip=True, required=False)
    ds_range = forms.CharField(max_length=72, strip=True, required=False)

