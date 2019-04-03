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
]