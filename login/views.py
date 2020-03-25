# coding:utf8

from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from login.models import Menu, RoleMenu


class LoginView(LoginView):

    def get(self, request):
        redirect = request.GET.get('next', '')
        return render(request, 'login/login.html', {'next': redirect})

    def post(self, request, *args, **kwargs):
        try:
            uname = request.POST['uname']
            upassword = request.POST['upassword']
            redirect = request.POST.get('next', '')
        except KeyError:
            return render(request, 'login/login.html', {'error_message': "Empty Input !", })
        user = authenticate(request, username=uname, password=upassword)
        # user = authenticate(request, uname='ted', upassword='000')
        if user is not None:
            login(request, user)
            user_name = request.user.username
            request.session['user_name'] = user_name
            user_group = Group.objects.get(user__username=user_name).name
            request.session['user_group'] = user_group
            if redirect:
                return HttpResponseRedirect(redirect)  # 转到登陆前页面
            else:
                return HttpResponseRedirect(reverse('projects:index', args=[1]))
        else:
            return render(request, 'login/login.html', {'error_message': "Permission Denied !", })


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:login'))

