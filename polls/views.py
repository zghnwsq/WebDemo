# coding:utf-8

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.contrib.auth.models import Group, User
from login.models import Menu, RoleMenu
# from django.db.models.expressions import RawSQL
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate,login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import OuterRef, Subquery, Exists
# from django.contrib.auth.models import User
# from django.http import Http404
#from django.templates import loader


class IndexView(LoginRequiredMixin, generic.ListView):
    # login_url = 'login/'
    # redirect_field_name
    # template_name = 'polls/index.html'
    # context_object_name = 'latest_question_list'  # 指定传入模板的context的名字

    # def get_queryset(self):
    #     """Return the last five published questions."""
    #     """Question.objects.filter(pub_date__lte=timezone.now())
    #     returns a queryset containing Questions whose pub_date is less than or equal to
    #     - that is, earlier than or equal to - timezone.now."""
    #     return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

    def get(self, request):
        latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
        # user_group = request.user.groups.name
        user_name = request.user.username
        user_group = Group.objects.get(user__username=user_name)
        rmenu = RoleMenu.objects.filter(role_name=user_group).values('menu')
        menu = Menu.objects.filter(menu_text__in=rmenu).order_by('order')
        context = {'latest_question_list': latest_question_list,
                   'menu':menu,
                   'user_group':user_group,
                   'user_name':user_name}
        return render(request, 'polls/index.html', context)



class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question  # 使用了模型, question自动提供给模板
    template_name = 'polls/detail.html'


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question  # 使用了模型, question自动提供给模板
    template_name = 'polls/results.html'


# class LoginView(LoginView):
#     # template_name = 'polls/login.html'
#
#     def get(self, request):
#         redirect = request.GET.get('next', '')
#         return render(request, 'polls/login.html', {'next': redirect})
#
#     def post(self, request, *args, **kwargs):
#         try:
#             uname = request.POST['uname']
#             upassword = request.POST['upassword']
#             redirect = request.POST.get('next', '')
#         except KeyError:
#             return render(request, 'polls/login.html', {'error_message': "Empty Input !", })
#         user = authenticate(request, username=uname, password=upassword)
#         # user = authenticate(request, uname='ted', upassword='000')
#         if user is not None:
#             login(request, user)
#             if redirect:
#                 return HttpResponseRedirect(redirect)  # 转到登陆前页面
#             else:
#                 return HttpResponseRedirect(reverse('polls:index'))
#         else:
#             return render(request, 'polls/login.html', {'error_message': "Premission Denined !", })


@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.POST['choice'] 以字符串形式返回选择的 Choice 的 ID。 request.POST 的值永远是字符串
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoseNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # reverse() 调用将返回一个这样的字符串：'/polls/question.id/results/'
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:login'))

# def index(request):
#     latest_question_list = Question.objects.order_by('pub_date')[:5]
#     # templates = loader.get_template('polls/index.html')  # 载入模板
#     context = {
#         'latest_question_list': latest_question_list,
#     }  # 要传入的变量
#     return render(request, 'polls/index.html', context)  # 返回模板装配后的网页
#
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
