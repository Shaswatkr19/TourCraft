from django.urls import path
from . import views
from django.shortcuts import redirect

app_name = 'tours'

urlpatterns = [
    path('', views.dashboard_view, name='tours_list'),   # ✅ Dashboard as main
    path('saved/', views.saved_tours_view, name='saved_tours'),

    # Steps related
    path('<int:tour_pk>/steps/create/', views.step_create_view, name='steps_create'),
    path('<int:tour_pk>/steps/<int:step_pk>/edit/', views.step_edit_view, name='step_edit'),
    path('<int:tour_pk>/steps/<int:step_pk>/delete/', views.step_delete_view, name='step_delete'),

    # Delete whole tour
    path('<int:pk>/delete/', views.tour_delete_view, name='tour_delete'),

    # API
    path('<int:pk>/api/', views.tour_api_data, name='tour_api_data'),
    path('create/enhanced/', views.EnhancedTourCreateView, name='enhanced_tour_create'),
    
]

