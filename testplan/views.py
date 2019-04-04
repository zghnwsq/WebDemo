import os, time
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.models import Group, User
from login.models import Menu, RoleMenu
from projects.models import ProjectsUser, Projects
from .models import TestCase
from datasource.models import Datasource
from django.http import JsonResponse
from .models import *
from .form import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.urls import reverse
# from TestCore.Main import *
from .runner import runcase
# Create your views here.

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'testplan/testplan.html'
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
        return HttpResponseRedirect(reverse('testplan:search_result', args=[project_id, 1]))
    except KeyError:
        context['message'] = 'Empty Input !'
        return render(request, 'testplan/testplan.html', context)


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
    testplan_list = TestPlan.objects.filter(project=selected)
    # print(testplan_list)
    paginator = Paginator(testplan_list, 10)
    try:
        testplan = paginator.page(page)
    except PageNotAnInteger:
        testplan = paginator.page(1)
    except EmptyPage:
        testplan = paginator.page(paginator.num_pages)
    if testplan:
        context['testplan_list'] = testplan
        return render(request, 'testplan/testplan.html', context)
    else:
        return render(request, 'testplan/testplan.html', context)


class ModifyView(LoginRequiredMixin, generic.FormView):
    template_name = 'testplan/modify.html'
    form_class = ModifyForm
    # success_url

    def get_data(self, request, testplan_id):
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
        testplan = TestPlan.objects.get(id=testplan_id)
        context['testplan'] = testplan
        case_list = TestCase.objects.filter(project_id=testplan.project_id)
        context['case_list'] = case_list
        datasource_list = Datasource.objects.filter(project_id=testplan.project_id)
        context['datasource_list'] = datasource_list
        return context

    def get(self, request, testplan_id):
        context = self.get_data(request, testplan_id)
        return render(request, 'testplan/modify.html', context)

    def post(self, request, testplan_id, *args, **kwargs):
        form = ModifyForm(request.POST)
        if form.is_valid():
            testplan = TestPlan.objects.get(id=testplan_id)
            no = request.POST['no']
            if no:
                testplan.no = no
            name = request.POST['name']
            if name:
                testplan.name = name
            cs = request.POST['testcase']
            if cs:
                case = TestCase.objects.get(id=cs)
                # print(case)
                testplan.case = case
            ds = request.POST['datasource']
            if ds:
                datasource = Datasource.objects.get(id=ds)
                # print(datasource)
                testplan.ds = datasource
            ip = request.POST['ip']
            if ip:
                testplan.ip = ip
            ds_range = request.POST['ds_range']
            if ds_range:
                testplan.ds_range = ds_range
            # 没有修改
            elif not no and not name and not ip and not ds_range and not case and not datasource:
                context = self.get_data(request, testplan_id)
                context['message'] = 'Nothing changed!'
                return render(request, 'testplan/modify.html', context)
            testplan.save()
            context = self.get_data(request, testplan_id)
            context['message'] = 'Success!'
            return render(request, 'testplan/modify.html', context)
        else:
            context = self.get_data(request, testplan_id)
            context['message'] = form.errors
            return render(request, 'testplan/modify.html', context)


class NewView(LoginRequiredMixin, generic.FormView):
    template_name = 'testplan/new.html'
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
        # case_list = TestCase.objects.filter(project_id__in=projects)
        # context['case_list'] = case_list
        # datasource_list = Datasource.objects.filter(project_id__in=projects)
        # context['datasource_list'] = datasource_list
        return context

    def get(self, request):
        context = self.get_data(request)
        return render(request, 'testplan/new.html', context)

    def post(self, request,*args, **kwargs):
        form = NewForm(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            no = request.POST['no']
            name = request.POST['name']
            pj = request.POST['project']
            project = Projects.objects.get(id=pj)
            cs = request.POST['testcase']
            if cs:
                testcase = TestCase.objects.get(id=cs)
            ds = request.POST['datasource']
            if ds:
                datasource = Datasource.objects.get(id=ds)
            if not project:
                context = self.get_data(request)
                context['message'] = 'Project Required !'
                return render(request, 'testplan/new.html', context)
            charge = User.objects.get(username=request.session['user_name'])
            ip = request.POST['ip']
            ds_range = request.POST['ds_range']
            testplan = TestPlan(no=no,
                                name=name,
                                project=project,
                                charge=charge,
                                case=testcase or None,
                                ds=datasource or None,
                                ip=ip,
                                ds_range=ds_range,
                                )
            testplan.save()
            context = self.get_data(request)
            context['testplan'] = testplan
            context['message'] = 'Success!'
            return render(request, 'testplan/new.html', context)
        else:
            context = self.get_data(request)
            context['message'] = form.errors
            return render(request, 'testplan/new.html', context)

def choice(request, project_id):
    case_set = TestCase.objects.filter(project_id=project_id)
    case_list = []
    for case in case_set:
        case_list.append({'id': str(case.id), 'name': case.case})
    ds_set = Datasource.objects.filter(project_id=project_id)
    datasource_list = []
    for ds in ds_set:
        datasource_list.append({'id': str(ds.id), 'name': ds.name})
    ret = {'case_list': case_list, 'datasource_list': datasource_list}
    return JsonResponse(ret)


@login_required
def delete(request, testplan_id):
    testplan = TestPlan.objects.get(id=testplan_id)
    selected_id = testplan.project_id
    # 清除任务执行记录和日志
    his = TP_Run_His.objects.filter(testplan_id=testplan.id)
    for h in his:
        detail = TP_Run_Detail.objects.filter(his_id=h.id)
        for d in detail:
            d.delete()
        base = os.path.join(settings.MEDIA_ROOT, 'log')
        if h.log_path:
            log = os.path.join(base, h.log_path)
            if os.path.isfile(log):
                os.remove(log)
        h.delete()
    testplan.delete()
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
    return render(request, 'testplan/testplan.html', context)


class DetailView(LoginRequiredMixin, generic.ListView):
    template_name = 'testplan/detail.html'
    context_object_name = 'testplan'

    def get_queryset(self, **kwargs):
        testplan_id = self.kwargs['testplan_id']
        testplan = TestPlan.objects.get(id=testplan_id)
        return testplan

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        user_group = request.session['user_group']
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        testplan_id = self.kwargs['testplan_id']
        testplan = TestPlan.objects.get(id=testplan_id)
        context['menu'] = menu
        context['user_group'] = request.session['user_group']
        context['user_name'] = request.session['user_name']
        context['project_id'] = self.kwargs['project_id']
        project = Projects.objects.get(id=testplan.project_id)
        context['project'] = project
        case = TestCase.objects.get(id=testplan.case_id)
        context['case'] = case or ''
        ds = Datasource.objects.get(id=testplan.ds_id)
        context['ds'] = ds or ''
        return context


@login_required
def run(request, testplan_id):
    testplan = TestPlan.objects.get(id=testplan_id)
    # 状态为空或者不为执行中
    if not testplan.status or testplan.status.find('执行中') == -1:
        stat = '1'
    else:
        stat = ''
    if testplan.case and testplan.ip and stat and TestCase.objects.get(id=testplan.case_id).path:
        case = TestCase.objects.get(id=testplan.case_id)
        ds = Datasource.objects.get(id=testplan.ds_id)
        ip = testplan.ip
        c_base = os.path.join(settings.MEDIA_ROOT, 'cases')
        case_path = os.path.join(c_base, case.path)
        case_sheet = case.sheet
        ds_range = testplan.ds_range or None
        ds_base = os.path.join(settings.MEDIA_ROOT, 'datasource')
        ds_path = os.path.join(ds_base, ds.path or '')
        ds_sheet = ds.sheet or None
        testplan.status = '执行中'
        testplan.save()
        runcase(testplan_id, case, case_path, case_sheet, ds_path=ds_path, ds_sheet=ds_sheet, ds_range=ds_range)
        return HttpResponseRedirect(reverse('testplan:search_result', args=[testplan.project_id, 1]))
    else:
        user_projects = ProjectsUser.objects.filter(user_id=request.user.id).values('project_id')
        project_list =  Projects.objects.filter(id__in=user_projects).filter(status='1')
        user_group = request.session['user_group']
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        context = {
            'menu': menu,
            'user_group': request.session['user_group'],
            'user_name': request.session['user_name'],
            'project_list': project_list,
            'error': '用例执行中 或者 未配置用例或ip 或 未导入用例!'
        }
        return render(request, 'testplan/testplan.html', context)


@login_required
def result(request, testplan_id):
    return HttpResponseRedirect(reverse('testplan:result_list', args=[testplan_id, 1]))


@login_required
def result_list(request, testplan_id, page):
    testplan = TestPlan.objects.get(id=testplan_id)
    project = Projects.objects.get(id=testplan.project_id)
    user_name = request.session['user_name']
    user_group = request.session['user_group']
    rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
    menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
    context = {'menu': menu,
               'user_group': user_group,
               'user_name': user_name,
               'project': project,
               }

    his_list = TP_Run_His.objects.filter(testplan_id=testplan_id).order_by('-update_time')
    paginator = Paginator(his_list, 10)
    try:
        his_list = paginator.page(page)
    except PageNotAnInteger:
        his_list = paginator.page(1)
    except EmptyPage:
        his_list = paginator.page(paginator.num_pages)
    if his_list:
        context['his_list'] = his_list
        return render(request, 'testplan/result.html', context)
    else:
        return render(request, 'testplan/result.html', context)


class LogView(LoginRequiredMixin, generic.ListView):
    template_name = 'testplan/log.html'
    context_object_name = 'log'

    def get_queryset(self, **kwargs):
        his_id = self.kwargs['his_id']
        his = TP_Run_His.objects.get(id=his_id)
        path = his.log_path
        base = os.path.join(settings.MEDIA_ROOT, 'log')
        log_path = os.path.join(base, path)
        log_html = []
        if os.path.isdir(base):
            if os.path.isfile(log_path):
                print(log_path)
                log = open(log_path, encoding='utf8')
                if log:
                    lines = log.readlines()
                    for line in lines:
                        log_html.append(line)
                    return log_html
                else:
                    return log_html
            else:
                return log_html
        else:
            return log_html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        user_group = request.session['user_group']
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        his_id = self.kwargs['his_id']
        his = TP_Run_His.objects.get(id=his_id)
        testplan = TestPlan.objects.get(id=his.testplan_id)
        context['menu'] = menu
        context['user_group'] = request.session['user_group']
        context['user_name'] = request.session['user_name']
        context['testplan'] = testplan
        return context


