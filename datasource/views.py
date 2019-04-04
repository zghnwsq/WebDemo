from django.shortcuts import render
import os
from django.shortcuts import render
from django.contrib.auth.models import Group, User
from login.models import Menu, RoleMenu
from projects.models import ProjectsUser, Projects
from .models import Datasource
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .form import *
from .handle_file import *
from django.conf import settings
from TestCore.Excel import Excel
# Create your views here.


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'datasource/datasource.html'
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
        return HttpResponseRedirect(reverse('datasource:search_result', args=[project_id, 1]))
    except KeyError:
        context['message'] = 'Empty Input !'
        return render(request, 'datasource/datasource.html', context)


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
    datasource_list = Datasource.objects.filter(project=selected).order_by('id')
    paginator = Paginator(datasource_list, 10)
    try:
        datasource = paginator.page(page)
    except PageNotAnInteger:
        datasource = paginator.page(1)
    except EmptyPage:
        datasource = paginator.page(paginator.num_pages)
    if datasource:
        context['datasource_list'] = datasource
        return render(request, 'datasource/datasource.html', context)
    else:
        return render(request, 'datasource/datasource.html', context)


class ModifyView(LoginRequiredMixin, generic.FormView):
    template_name = 'datasource/modify.html'
    form_class = ModifyForm
    # success_url

    def get_data(self, request, datasource_id):
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
        datasource = Datasource.objects.get(id=datasource_id)
        context['datasource'] = datasource
        return context

    def get(self, request, datasource_id):
        context = self.get_data(request, datasource_id)
        return render(request, 'datasource/modify.html', context)

    def post(self, request, datasource_id, *args, **kwargs):
        form = ModifyForm(request.POST, request.FILES)
        if form.is_valid():
            datasource = Datasource.objects.get(id=datasource_id)
            no = request.POST['no']
            if no:
                datasource.no = no
            name = request.POST['datasource']
            if name:
                datasource.name = name
            sheet = request.POST['sheet']
            if sheet:
                datasource.sheet = sheet
            if 'file' in request.FILES.keys():
                if request.FILES['file'].name.find('.xls') == -1:
                    context = self.get_data(request, datasource_id)
                    context['message'] = 'Wrong file type!'
                    return render(request, 'datasource/modify.html', context)
                file_path = handle_uploaded_case(request.FILES['file'], datasource.project_id, datasource_id)
                datasource.path = file_path
                sheet = request.POST['sheet']
                if not sheet:
                    context = self.get_data(request, datasource_id)
                    context['message'] = 'Empty sheet name!'
                    return render(request, 'datasource/modify.html', context)
                base = os.path.join(settings.MEDIA_ROOT, 'datasource')
                excel = Excel.read_sheet(os.path.join(base, file_path), sheet)
                datasource.length = len(excel[0])-1
            # 没有修改
            elif not no and not datasource and not sheet and 'file' not in request.FILES.keys():
                context = self.get_data(request, datasource_id)
                context['message'] = 'Nothing changed!'
                return render(request, 'datasource/modify.html', context)
            datasource.save()
            context = self.get_data(request, datasource_id)
            context['message'] = 'Success!'
            return render(request, 'datasource/modify.html', context)
        else:
            context = self.get_data(request, datasource_id)
            context['message'] = form.errors
            return render(request, 'datasource/modify.html', context)


class NewView(LoginRequiredMixin, generic.FormView):
    template_name = 'datasource/new.html'
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
        return context

    def get(self, request):
        context = self.get_data(request)
        return render(request, 'datasource/new.html', context)

    def post(self, request, *args, **kwargs):
        form = NewForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            no = request.POST['no']
            datasource = request.POST['datasource']
            pj = request.POST['project']
            project = Projects.objects.get(id=pj)
            charge = User.objects.get(username=request.session['user_name'])
            datasource = Datasource(no=no, name=datasource, project=project, charge=charge)
            datasource.save()
            if 'file' in request.FILES.keys():
                if request.FILES['file'].name.find('.xls') == -1:
                    context = self.get_data(request)
                    context['message'] = 'Wrong file type!'
                    return render(request, 'datasource/new.html', context)
                file_path = handle_uploaded_case(request.FILES['file'], project.id, datasource.id)
                datasource.path = file_path
                sheet = request.POST['sheet']
                if sheet:
                    datasource.sheet = sheet
                else:
                    context = self.get_data(request)
                    context['message'] = 'Empty sheet name!'
                    return render(request, 'datasource/new.html', context)
                base = os.path.join(settings.MEDIA_ROOT, 'datasource')
                excel = Excel.read_sheet(os.path.join(base, file_path), sheet)
                datasource.length = len(excel[0]) - 1
                datasource.save()
            context = self.get_data(request)
            context['datasource'] = datasource
            context['message'] = 'Success!'
            return render(request, 'datasource/new.html', context)
        else:
            context = self.get_data(request)
            context['message'] = form.errors
            return render(request, 'datasource/new.html', context)


@login_required
def delete(request, datasource_id):
    datasource = Datasource.objects.get(id=datasource_id)
    selected_id = datasource.project_id
    if datasource.path:
        datasource_path = os.path.join('datasource',datasource.path)
        file_path = os.path.join(settings.MEDIA_ROOT, datasource_path)
        # print(file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)
    datasource.delete()
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
    return render(request, 'datasource/datasource.html', context)


class DetailView(LoginRequiredMixin, generic.ListView):
    template_name = 'datasource/detail.html'
    context_object_name = 'excel'

    def get_queryset(self, **kwargs):
        datasource_id = self.kwargs['datasource_id']
        datasource = Datasource.objects.get(id=datasource_id)
        path = datasource.path
        sheet = datasource.sheet
        base = os.path.join(settings.MEDIA_ROOT, 'datasource')
        if path and sheet:
            path = os.path.join(base, path)
            if os.path.isfile(path):
                excel = Excel.read_sheet(path, sheet)
                if excel:
                    return excel
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
        datasource_id = self.kwargs['datasource_id']
        datasource = Datasource.objects.get(id=datasource_id)
        context['menu'] = menu
        context['user_group'] = request.session['user_group']
        context['user_name'] = request.session['user_name']
        context['datasource'] = datasource
        context['project_id'] = self.kwargs['project_id']
        return context


