from django.urls import path
from . import views

app_name = 'testcase'
urlpatterns = [
    path('', views.IndexView.as_view(), name='testcase'),
    path('search/', views.search, name='search'),
]

