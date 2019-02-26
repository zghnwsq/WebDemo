from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


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
            if redirect:
                return HttpResponseRedirect(redirect)  # 转到登陆前页面
            else:
                return HttpResponseRedirect(reverse('polls:index'))
        else:
            return render(request, 'login/login.html', {'error_message': "Premission Denined !", })