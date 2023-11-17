from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, PolicyViewSet, CustomerPolicyViewSet

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"policies", PolicyViewSet, basename="policy")
router.register(r"customer_policies", CustomerPolicyViewSet, basename="customer_policies")

urlpatterns = [
    path("api/", include(router.urls)),
]
