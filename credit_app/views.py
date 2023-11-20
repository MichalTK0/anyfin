from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from .models import Customer, Policy, CustomerPolicy
from .serializers import CustomerSerializer, PolicySerializer, CustomerPolicySerializer


class SimpleViewSet(viewsets.ModelViewSet):
    """
    Custom API ViewSet
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            # Create the model to surface the primary key, returned as the ID in the resp.
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        except serializers.ValidationError as e:

            response_data = {
                "message": "REJECT",
                "reason": e.detail
            }

            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            "message": "ACCEPT",
            "detail": serializer.data
        }

        response_data["detail"]["id"] = serializer.instance.pk
        return Response(response_data, status=status.HTTP_201_CREATED)


class CustomerViewSet(SimpleViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class PolicyViewSet(SimpleViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class CustomerPolicyViewSet(viewsets.ModelViewSet):
    queryset = CustomerPolicy.objects.all()
    serializer_class = CustomerPolicySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            # Create the model to surface the primary key, returned as the ID in the resp.
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            if not serializer.instance.accepted:

                response_data = {
                    "message": "REJECT",
                    "detail": serializer.data,
                    "reason": serializer.instance.rejection_reason
                }

            else:
                response_data = {
                    "message": "ACCEPT",
                    "detail": serializer.data
                }

            response_data["detail"]["id"] = serializer.instance.pk
            return Response(response_data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError as e:

            response_data = {
                "message": "REJECT",
                "reason": e.detail
            }

            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
