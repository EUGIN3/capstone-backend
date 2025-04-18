from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {
            'password' : {'write_only':True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def to_representation(self, instance):
        to_return = super().to_representation(instance)
        to_return.pop('password', None)
        return to_return

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to return all users. Excludes sensitive fields like password.
    """
    class Meta:
        model = User
        # Exclude password and other sensitive information
        exclude = ('password',)
        # If you prefer to list specific fields, you can use:
        # fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']




