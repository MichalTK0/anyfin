from rest_framework import serializers
from .models import Customer, Policy, CustomerPolicy


class CustomerSerializer(serializers.ModelSerializer):
    """Basic customer model serializer."""
    class Meta:
        model = Customer
        fields = "__all__"


class PolicySerializer(serializers.ModelSerializer):
    """Basic policy model serializer"""
    class Meta:
        model = Policy
        fields = "__all__"


class CustomerPolicySerializer(serializers.ModelSerializer):
    """
    Customer Policy model serializer
    Forces a full clean on the serializer model so acceptance and rejection reasons (if any) can be appropriately
    generated in the full_clean method.
    """
    class Meta:
        model = CustomerPolicy
        fields = "__all__"

    def validate(self, data):
        instance = CustomerPolicy(**data)
        instance.full_clean()
        return data
