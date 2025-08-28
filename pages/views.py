# pages/views.py
from django.shortcuts import render

def landing_page(request):
    return render(request, 'base/landing_simple.html')

def about_page(request):
    return render(request, 'pages/about.html')

def contact_page(request):
    return render(request, 'pages/contact.html')