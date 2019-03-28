from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, User
from login.models import Menu, RoleMenu
from projects.models import ProjectsUser, Projects
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import TestCase
from django.contrib.auth.decorators import login_required
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
        case_list = TestCase.objects.filter(project=project_id)
        if case_list:
            context['case_list'] = case_list
            return render(request, 'testcase/testcase.html', context)
        else:
            return render(request, 'testcase/testcase.html', context)
    except KeyError:
        context['error_message'] = 'Empty Input !'
        return render(request, 'testcase/testcase.html', context)



