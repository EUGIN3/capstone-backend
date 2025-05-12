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

    # Not required fields in registration
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


# class AppointmentInformation(models.Model):
#     date = models.CharField(max_length=100)
#     time = models.CharField(max_length=100)
#     image = models.ImageField(upload_to='appointments/')
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     address = models.TextField()
#     phone_number = models.CharField(max_length=20)
#     facebook_link = models.CharField(max_length=255)
#     description = models.TextField()
#     date_set = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} - {self.date}"
    

# Appointment class.
class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='appointments')
    name = models.CharField(max_length=100)
    time = models.TimeField()
    date = models.DateField()
    phone_number = models.CharField(max_length=15)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='appointment_images/', blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"

    @property
    def email(self):
        return self.user.email
    










    
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