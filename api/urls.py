from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tours.api_views import TourViewSet
from accounts.api_views import UserViewSet

app_name = "api"

router = DefaultRouter()
router.register(r'tours', TourViewSet, basename='tour')
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]