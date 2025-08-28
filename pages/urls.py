# pages/urls.py
from django.urls import path
from . import views

app_name = 'pages'  # optional, but recommended

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact_page, name='contact'),
]