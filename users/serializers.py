from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'phone_number', 'is_driver')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
