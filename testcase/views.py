# coding:utf8

import os
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, User
from login.models import Menu, RoleMenu
from projects.models import ProjectsUser, Projects
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import TestCase
from testcase.form import ModifyForm, NewForm
# from django.views.generic.edit import FormView
# from datasource.models import Datasource
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import  HttpResponseRedirect
from django.urls import reverse
from .handle_file import handle_uploaded_case
from django.conf import settings
from TestCore.Excel import Excel
# Create your views here.


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'testcase/testcase.html'
    context_object_name = 'project_list'

    def get_queryset(self):
        user_projects = ProjectsUser.objects.filter(user_id=self.request.user.id).values('project_id')
        return Projects.objects.filter(id__in=user_projects).filter(status='1')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user_name = self.request.user.username
        user_group = self.request.session['user_group']
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        context['menu'] = menu
        context['user_group'] = self.request.session['user_group']
        context['user_name'] = self.request.session['user_name']
        return context


@login_required
def search(request):
    user_projects = ProjectsUser.objects.filter(user_id=request.user.id).values('project_id')
    project_list = Projects.objects.filter(id__in=user_projects).filter(status='1')
    # user_name = request.user.username
    user_group = request.session['user_group']
    rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
    menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
    user_name = request.session['user_name']
    user_group = request.session['user_group']
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
        context['message'] = 'Empty Input !'
        return render(request, 'testcase/testcase.html', context)


@login_required
def search_result(request, selected, page):
    user_projects = ProjectsUser.objects.filter(user_id=request.user.id).values('project_id')
    project_list = Projects.objects.filter(id__in=user_projects).filter(status='1')
    user_name = request.session['user_name']
    user_group = request.session['user_group']
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

    def get_data(self, request, case_id):
        user_name = request.session['user_name']
        user_group = request.session['user_group']
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
        return context

    def get(self, request, case_id):
        context = self.get_data(request, case_id)
        return render(request, 'testcase/modify.html', context)

    def post(self, request, case_id, *args, **kwargs):
        form = ModifyForm(request.POST, request.FILES)
        if form.is_valid():
            testcase = TestCase.objects.get(id=case_id)
            no = request.POST['no']
            if no:
                testcase.no = no
            case = request.POST['case']
            if case:
                testcase.case = case
            # project = request.POST['project']
            # if project:
            #     testcase.project = Projects.objects.get(id=project)
            # print(request.FILES['file'].name)
            if 'file' in request.FILES.keys():
                if request.FILES['file'].name.find('.xls') == -1:
                    context = self.get_data(request, case_id)
                    context['message'] = 'Wrong file type!'
                    return render(request, 'testcase/modify.html', context)
                file_path = handle_uploaded_case(request.FILES['file'], testcase.project_id, case_id)
                testcase.path = file_path
                sheet = request.POST['sheet']
                if sheet:
                    testcase.sheet = sheet
                else:
                    context = self.get_data(request, case_id)
                    context['message'] = 'Empty sheet name!'
                    return render(request, 'testcase/modify.html', context)
            # 没有修改
            elif not no and not case and 'file' not in request.FILES.keys():
                context = self.get_data(request, case_id)
                context['message'] = 'Nothing changed!'
                return render(request, 'testcase/modify.html', context)
            testcase.save()
            context = self.get_data(request, case_id)
            context['message'] = 'Success!'
            return render(request, 'testcase/modify.html', context)
        else:
            context = self.get_data(request, case_id)
            context['message'] = form.errors
            return render(request, 'testcase/modify.html', context)


class NewView(LoginRequiredMixin, generic.FormView):
    template_name = 'testcase/new.html'
    form_class = NewForm

    def get_data(self, request):
        user_name = request.session['user_name']
        user_group = request.session['user_group']
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
        # testcase = TestCase.objects.get(id=case_id)
        # context['testcase'] = testcase
        return context

    def get(self, request):
        context = self.get_data(request)
        return render(request, 'testcase/new.html', context)

    def post(self, request,*args, **kwargs):
        form = NewForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            no = request.POST['no']
            case = request.POST['case']
            pj = request.POST['project']
            project = Projects.objects.get(id=pj)
            # if not no and not case and not project:
            #     context = self.get_data(request)
            #     context['message'] = 'Empty Input !'
            #     return render(request, 'testcase/new.html', context)
            charge = User.objects.get(username=request.session['user_name'])
            testcase = TestCase(no=no, case=case, project=project, charge=charge)
            testcase.save()
        # testcase = TestCase.objects.get(no=no)
            if 'file' in request.FILES.keys():
                if request.FILES['file'].name.find('.xls') == -1:
                    context = self.get_data(request)
                    context['message'] = 'Wrong file type!'
                    return render(request, 'testcase/new.html', context)
                file_path = handle_uploaded_case(request.FILES['file'], project.id, testcase.id)
                testcase.path = file_path
                sheet = request.POST['sheet']
                if sheet:
                    testcase.sheet = sheet
                else:
                    context = self.get_data(request)
                    context['message'] = 'Empty sheet name!'
                    return render(request, 'testcase/new.html', context)
                testcase.save()
            context = self.get_data(request)
            context['testcase'] = testcase
            context['message'] = 'Success!'
            return render(request, 'testcase/new.html', context)
        else:
            context = self.get_data(request)
            context['message'] = form.errors
            return render(request, 'testcase/new.html', context)


@login_required
def delete(request, case_id):
    testcase = TestCase.objects.get(id=case_id)
    selected_id = testcase.project_id
    if testcase.path:
        case_path = os.path.join('cases',testcase.path)
        file_path = os.path.join(settings.MEDIA_ROOT, case_path)
        # print(file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)
    testcase.delete()
    user_projects = ProjectsUser.objects.filter(user_id=request.user.id).values('project_id')
    project_list = Projects.objects.filter(id__in=user_projects)
    user_group = request.session['user_group']
    rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
    menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
    user_name = request.session['user_name']
    user_group = request.session['user_group']
    context = {'menu': menu,
               'user_group': user_group,
               'user_name': user_name,
               'selected_id': selected_id,
               'project_list': project_list,
               'message': 'Delete success!'
               }
    return render(request, 'testcase/testcase.html', context)


class DetailView(LoginRequiredMixin, generic.ListView):
    template_name = 'testcase/detail.html'
    context_object_name = 'case'

    def get_queryset(self, **kwargs):
        case_id = self.kwargs['case_id']
        testcase = TestCase.objects.get(id=case_id)
        path = testcase.path
        sheet = testcase.sheet
        base = os.path.join(settings.MEDIA_ROOT, 'cases')
        if path and sheet:
            path = os.path.join(base, path)
            if os.path.isfile(path):
                case = Excel.read_sheet(path, sheet)
                if case:
                    return case
                    # print(case)
                else:
                    return None
            else:
                return None
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        user_group = request.session['user_group']
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        case_id = self.kwargs['case_id']
        testcase = TestCase.objects.get(id=case_id)
        context['menu'] = menu
        context['user_group'] = request.session['user_group']
        context['user_name'] = request.session['user_name']
        context['testcase'] = testcase
        context['project_id'] = self.kwargs['project_id']
        return context







