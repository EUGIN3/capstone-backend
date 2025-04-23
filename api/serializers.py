from rest_framework import serializers
from . import models
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


class AppointmentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = models.Appointment
        fields = ['id', 'name', 'time', 'date', 'phone_number', 'email', 'description', 'image', 'is_approved']