from django.urls import path
from . import views

app_name = 'projects'
urlpatterns = [
    path('page/<int:page>', views.IndexView.as_view(), name='index'),
    path('<int:pk>/modify/', views.ModifyView.as_view(), name='modify'),
]

