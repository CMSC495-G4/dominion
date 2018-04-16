from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('rules/', views.rules, name='rules'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('history/', views.history, name='history'),
    path('play/', views.play, name='play'),
    path('logout/', views.logout),
]
