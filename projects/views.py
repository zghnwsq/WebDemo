from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Projects, ProjectsUser
from django.contrib.auth.models import Group, User
from login.models import Menu, RoleMenu


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
        # user_projects = ProjectsUser.objects.filter(user=request.user.id).values('project')
        # project_list = Projects.objects.filter(project__in=user_projects)
        # context['user_projects'] = user_projects
        return context