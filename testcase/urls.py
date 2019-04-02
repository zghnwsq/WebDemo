from django.urls import path
from . import views

app_name = 'testcase'
urlpatterns = [
    path('', views.IndexView.as_view(), name='testcase'),
    path('search/', views.search, name='search'),
    path('search/<int:selected>/<int:page>', views.search_result, name='search_result'),
    path('<int:case_id>/modify/', views.ModifyView.as_view(), name='modify'),
    path('<int:case_id>/delete/', views.delete, name='delete'),
    path('new/', views.NewView.as_view(), name='new'),
    path('<int:project_id>/<int:case_id>/detail/', views.DetailView.as_view(), name='detail'),
]

