from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
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


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'last_name',
            'address',
            'facebook_link',
            'is_staff',
            'is_superuser',
        ]
        read_only_fields = fields
        

class AppointmentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = models.Appointment
        fields = '__all__'
        read_only_fields = ['user']



class UnavailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Unavailability
        fields = [
            'id',
            'date',
            'slot_one',
            'slot_two',
            'slot_three',
            'slot_four',
            'slot_five',
        ]
