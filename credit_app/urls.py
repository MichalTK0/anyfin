# urls.py in your_app

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('api/', include(router.urls)),  # Set the base URL here
    # Add any additional paths if needed
]
