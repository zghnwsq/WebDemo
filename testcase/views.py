# coding:utf8

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, User
from login.models import Menu, RoleMenu
from projects.models import ProjectsUser, Projects
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import TestCase
from testcase.modify import ModifyForm
from django.views.generic.edit import FormView
# from datasource.models import Datasource
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import  HttpResponseRedirect
from django.urls import reverse
# Create your views here.


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'testcase/testcase.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        user_projects = ProjectsUser.objects.filter(user_id=self.request.user.id).values('project_id')
        return Projects.objects.filter(id__in=user_projects)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_name = self.request.user.username
        user_group = Group.objects.get(user__username=user_name)
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        context['menu'] = menu
        context['user_group'] = user_group
        context['user_name'] = user_name
        return context


@login_required
def search(request):
    user_projects = ProjectsUser.objects.filter(user_id=request.user.id).values('project_id')
    project_list = Projects.objects.filter(id__in=user_projects)
    user_name = request.user.username
    user_group = Group.objects.get(user__username=user_name)
    rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
    menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
    context = {'menu': menu,
               'user_group': user_group,
               'user_name': user_name,
               'project_list': project_list
               }
    try:
        project_id = request.POST['project']
        context['selected_id'] = project_id
        return HttpResponseRedirect(reverse('testcase:search_result', args=[project_id, 1]))
    except KeyError:
        context['error_message'] = 'Empty Input !'
        return render(request, 'testcase/testcase.html', context)


@login_required
def search_result(request, selected, page):
    user_projects = ProjectsUser.objects.filter(user_id=request.user.id).values('project_id')
    project_list = Projects.objects.filter(id__in=user_projects)
    user_name = request.user.username
    user_group = Group.objects.get(user__username=user_name)
    rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
    menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
    context = {'menu': menu,
               'user_group': user_group,
               'user_name': user_name,
               'project_list': project_list,
               'selected_id': selected
               }
    case_list = TestCase.objects.filter(project=selected)
    paginator = Paginator(case_list, 10)
    try:
        cases = paginator.page(page)
    except PageNotAnInteger:
        cases = paginator.page(1)
    except EmptyPage:
        cases = paginator.page(paginator.num_pages)
    if cases:
        context['case_list'] = cases
        return render(request, 'testcase/testcase.html', context)
    else:
        return render(request, 'testcase/testcase.html', context)



class ModifyView(LoginRequiredMixin, generic.FormView):
    template_name = 'testcase/modify.html'
    form_class = ModifyForm
    # success_url

    def get(self, request, case_id):
        user_name = request.user.username
        user_group = Group.objects.get(user__username=user_name)
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        context = {
            'menu': menu,
            'user_group': user_group,
            'user_name': user_name,
        }
        user_projects = ProjectsUser.objects.filter(user_id=self.request.user.id).values('project_id')
        projects = Projects.objects.filter(id__in=user_projects).filter(status='1')
        context['projects'] = projects
        testcase = TestCase.objects.get(id=case_id)
        context['testcase'] = testcase
        return render(request, 'testcase/modify.html', context)



