from rest_framework import serializers
from .models import Customer, Policy, CustomerPolicy


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = "__all__"


class CustomerPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPolicy
        fields = "__all__"

    def validate(self, data):
        instance = CustomerPolicy(**data)
        instance.full_clean()
        return data
