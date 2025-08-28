from django.urls import path
from . import views

app_name = 'tours'

urlpatterns = [
    path('saved/', views.saved_tours_view, name='saved_tours'),
    path('', views.tour_list, name='tours_list'),
    path('create/', views.tour_create_view, name='tour_create'),
    path('create/enhanced/', views.tour_create_enhanced_view, name='tour_create_enhanced'),
    path('<int:pk>/', views.tour_detail_view, name='tour_detail'),
    path('<int:pk>/edit/', views.tour_edit_view, name='tour_edit'),
    path('<int:pk>/delete/', views.tour_delete_view, name='tour_delete'),
    path('<int:pk>/preview/', views.tour_preview_view, name='tour_preview'),
    path('<int:pk>/preview/enhanced/', views.tour_preview_enhanced_view, name='tour_preview_enhanced'),
    path('<int:pk>/preview/enhanced/v2/', views.tour_preview_enhanced_v2_view, name='tour_preview_enhanced_v2'),
    path('<int:pk>/share/', views.tour_share_view, name='tour_share'),
    path('<int:pk>/steps/', views.tour_steps_view, name='tour_steps'),
    path('<int:tour_pk>/steps/create/', views.step_create_view, name='steps_create'),
    path('<int:tour_pk>/steps/<int:step_pk>/edit/', views.step_edit_view, name='step_edit'),
    path('<int:tour_pk>/steps/<int:step_pk>/delete/', views.step_delete_view, name='step_delete'),
    path('public/<uuid:tour_uuid>/', views.tour_public_view, name='tour_public_view'),
]