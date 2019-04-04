from django.urls import path
from . import views

app_name = 'testplan'
urlpatterns = [
    path('', views.IndexView.as_view(), name='testplan'),
    path('search/', views.search, name='search'),
    path('search/<int:selected>/<int:page>', views.search_result, name='search_result'),
    path('<int:testplan_id>/modify/', views.ModifyView.as_view(), name='modify'),
    path('<int:testplan_id>/delete/', views.delete, name='delete'),
    path('new/', views.NewView.as_view(), name='new'),
    path('<int:project_id>/<int:testplan_id>/detail/', views.DetailView.as_view(), name='detail'),
    path('<int:project_id>/choice', views.choice, name='choice'),
    path('<int:testplan_id>/run', views.run, name='run'),
    path('<int:testplan_id>/result/', views.result, name='result'),
    path('<int:testplan_id>/result/<int:page>', views.result_list, name='result_list'),
    path('<int:testplan_id>/result/<int:his_id>/log/', views.LogView.as_view(), name='log'),
]