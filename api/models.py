from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.html import strip_tags
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is a required field!')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=200, null=True, blank=True)

    first_name  = models.CharField(max_length=500, null=True, blank=True)
    last_name = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)

    phone_number = models.CharField(max_length=20, null=True, blank=True)
    facebook_link = models.CharField(max_length=500, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

# Appointment class.
class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')

    date = models.DateField()  # Handles dates like 2025-05-14
    time = models.CharField(max_length=255, null=True, blank=True) 

    image = models.ImageField(upload_to='appointment_images/', null=True, blank=True)
    address = models.TextField(max_length=500, null=True, blank=True)
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    appointment_status = models.CharField(max_length=100, default='pending')

    # Automatically set when the appointment is created
    date_set = models.DateTimeField(auto_now_add=True)

    @property
    def email(self):
        return self.user.email
    
    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def phone_number(self):
        return self.user.phone_number  
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.date}"





    
# For sending an email for forgot password.
@receiver(reset_password_token_created)
def password_reset_token_created(reset_password_token, *args, **kwargs):
    sitelink = "http://localhost:5173/"
    token = "{}".format(reset_password_token.key)
    full_link = str(sitelink)+str("reset-password/")+str(token)
    
    context = {
        'full_link' : full_link,
        'email_address' : reset_password_token.user.email,
    }

    html_message = render_to_string("reset_password_email.html", context=context)
    plain_message = strip_tags(html_message)

    msg = EmailMultiAlternatives(
        subject= "Request for resetting password for {title}".format(title=reset_password_token.user.email),
        body=plain_message,
        from_email="sender@example.com",
        to={reset_password_token.user.email},
    )

    msg.attach_alternative(html_message, "text/html")
    msg.send()