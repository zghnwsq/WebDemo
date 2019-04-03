from django.urls import path
from . import views

app_name = 'datasource'
urlpatterns = [
    path('', views.IndexView.as_view(), name='datasource'),
    path('search/', views.search, name='search'),
    path('search/<int:selected>/<int:page>', views.search_result, name='search_result'),
    path('<int:datasource_id>/modify/', views.ModifyView.as_view(), name='modify'),
    path('new/', views.NewView.as_view(), name='new'),
    path('<int:datasource_id>/delete', views.delete, name='delete'),
    path('<int:project_id>/<int:datasource_id>/detail', views.DetailView.as_view(), name='detail'),

]