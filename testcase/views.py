from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, User
from login.models import Menu, RoleMenu
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
# Create your views here.

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'projects/index.html'
    context_object_name = 'case_list'




