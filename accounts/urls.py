# accounts/urls.py - FIXED VERSION
from django.urls import path
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    # Root path - login page
    path('', views.login_view, name='login'),  # Main login page
    
    # Authentication
    path('login/', views.login_view, name='login_alt'),  # Alternative login URL
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    
    # Dashboard and profile
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('team/', views.team_view, name='team'),
    
    # Enhanced tour creation (main feature)
    path('tours/create/enhanced/', views.create_enhanced_tour, name='create_enhanced_tour'),
    path('tours/list/', views.tours_list_view, name='tours_list'),

    # path('', include('django.contrib.auth.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
 
]
