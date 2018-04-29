from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import forms, views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/games/', views.api_games, name='api_games'),
    path('api/player/<id>', views.api_player, name='api_player'),

    path('rules/', views.rules, name='rules'),
    path('about/', views.about, name='about'),

    # lobby
    path('play/', views.play, name='play'),
    
    # game session (same as history id, reused for channels)
    path('play/<id>', views.play_session, name='play_session'),

    path('profile/', views.profile, name='profile'),
    path('history/', views.GameListView.as_view(), name='history'),

    # login/logout/registration forms
    path('login/', auth_views.login, {'authentication_form': forms.LoginForm}, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    # password change forms (password_change_form.html, password_change_done.html)
    path('password/change/', auth_views.password_change, name='password_change'),
    path('password/change/done', auth_views.password_change_done, name='password_change_done'),

    # forms to request a password reset (password_reset_form.html, password_reset_done.html)
    path('password/reset/', auth_views.password_reset, name='password_reset'),
    path('password/reset/requested', auth_views.password_reset_done, name='password_reset_done'),

    # forms to reset a password (password_reset_confirm.html, password_reset_complete.html)
    path('password/reset/<uidb64>/<token>', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('password/reset/done', auth_views.password_reset_complete, name='password_reset_complete'),
]


