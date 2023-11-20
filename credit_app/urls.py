from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet, PolicyViewSet, CustomerPolicyViewSet
from django.views.generic import RedirectView

router = DefaultRouter()
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"policies", PolicyViewSet, basename="policy")
router.register(r"customer_policies", CustomerPolicyViewSet, basename="customer_policies")

urlpatterns = [
    path("api/", include(router.urls)),
    # Redirect root URL to admin page
    path('', RedirectView.as_view(url='/admin/', permanent=True)),
]
