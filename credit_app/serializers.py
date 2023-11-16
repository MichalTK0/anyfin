from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def validate(self, data):
        instance = Customer(**data)
        try:
            instance.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return data
