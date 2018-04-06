from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rules/', views.rules, name='rules'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
]