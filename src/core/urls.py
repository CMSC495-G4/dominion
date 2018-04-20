from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from . import forms

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.login, {'authentication_form': forms.LoginForm}, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),

    path('password-reset/', auth_views.password_reset, name='password_reset'),

    path('rules/', views.rules, name='rules'),
    path('about/', views.about, name='about'),
    path('play/', views.play, name='play'),

]
