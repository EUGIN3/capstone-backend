from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import get_user_model, authenticate
from . import serializers
from . import models

User = get_user_model()

class RegisterViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginViewset(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            if user:
                _, token = AuthToken.objects.create(user)

                user_data = serializers.UserInfoSerializer(user).data

                return Response(
                    {
                        'user': user_data,
                        'token': token,
                    }
                )
            else:
                return Response({"error":"Invalid Credentials",}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

class UserViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        queryset = User.objects.all()
        serializer = serializers.UserInfoSerializer(queryset, many=True)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        serializer = serializers.UserInfoSerializer(user)
        return Response(serializer.data)
    

class SetAppointmentViewSet(viewsets.ViewSet):
    serializer_class = serializers.AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user = request.user)

            return Response(
                {"message": "Appointment created successfully"},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class AppointmentsListViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        appointments = models.Appointment.objects.all()
        serializer = serializers.AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    def partial_update(self, request, pk=None):
        try:
            appointment = models.Appointment.objects.get(pk=pk)
        except models.Appointment.DoesNotExist:
            return Response(
                {"detail": "Appointment not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.AppointmentSerializer(appointment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAppointmentsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        user = request.user
        appointments = models.Appointment.objects.filter(user=user)
        serializer = serializers.AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
        
    def partial_update(self, request, pk=None):
        appointment = models.Appointment.objects.get(pk=pk, user=request.user)
        
        # Make a mutable copy of request data
        data = request.data.copy()

        data.pop('appointment_status', None)

        serializer = serializers.AppointmentSerializer(appointment, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        appointment = models.Appointment.objects.get(pk=pk, user=request.user)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UnavailabilityViewSet(viewsets.ModelViewSet):
    queryset = models.Unavailability.objects.all()
    serializer_class = serializers.UnavailabilitySerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        date = request.data.get("date")
        if not date:
            return Response({"error": "Date is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if an unavailability entry already exists for the date
            instance = models.Unavailability.objects.get(date=date)
            serializer = self.get_serializer(instance, data=request.data)
        except models.Unavailability.DoesNotExist:
            # If it doesn't exist, create a new one
            serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()

        