# tourcraft/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts import views as account_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('tours/', include(('tours.urls', 'tours'), namespace='tours')),
    path('', include('django.contrib.auth.urls')),  # Login/logout URLs

    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('login/', account_views.login_view, name='login'),
    
    # Remove this conflicting line:
    path('', include(('accounts.urls', 'root_accounts'), namespace='root_accounts')),
    
    # Keep pages at the end for homepage
    path('', include('pages.urls')),  # This will handle homepage
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)