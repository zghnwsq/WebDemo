# coding:utf8

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Projects, ProjectsUser
from django.contrib.auth.models import Group, User
from login.models import Menu, RoleMenu
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'projects/index.html'
    context_object_name = 'project_list'  # 指定传入模板的context的名字

    def get_queryset(self):
        user_projects = ProjectsUser.objects.filter(user_id=self.request.user.id).values('project_id')
        return Projects.objects.filter(id__in=user_projects)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        request = self.request
        user_name = request.user.username
        user_group = Group.objects.get(user__username=user_name)
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        context['menu'] = menu
        context['user_group'] = user_group
        context['user_name'] = user_name
        return context


class ModifyView(LoginRequiredMixin, generic.DetailView):
    template_name = 'projects/modify.html'
    # context_object_name = 'project_list'  # 指定传入模板的context的名字
    model = Projects

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        request = self.request
        user_name = request.user.username
        user_group = Group.objects.get(user__username=user_name)
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        context['menu'] = menu
        context['user_group'] = user_group
        context['user_name'] = user_name
        return context

    def post(self, request, pk):
        project = get_object_or_404(Projects, pk=pk)
        if self.request.POST['project'] != '':
            project.project = self.request.POST['project']
        if self.request.POST['status'] != '':
            project.status = self.request.POST['status']
        if self.request.POST['project'] == '' or self.request.POST['status'] == '':
            return render(self.request, 'projects/modify.html', {
                'message': 'Empty Input'
            })
        project.save()
        project = get_object_or_404(Projects, pk=pk)
        user_name = request.user.username
        user_group = Group.objects.get(user__username=user_name)
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        # return HttpResponseRedirect(reverse('projects:index'))
        context = {'message': '修改成功',
                   'projects': project,
                   'menu': menu,
                   'user_group': user_group,
                   'user_name': user_name
                   }
        return render(request, 'projects/modify.html', context)




