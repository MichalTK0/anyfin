# views.py

from rest_framework import viewsets, status, serializers
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            errors = {}
            for key, value in e.detail.items():
                errors[key] = value[0]
            response_data = {
                "message": "REJECT",
                "reason": errors
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response({"message": "ACCEPT"}, status=status.HTTP_201_CREATED, headers=headers)
