from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    GENDER_VALID_CHOICES = (
        (0, 'MALE'),
        (1, 'FEMALE'),
    )

    name = models.CharField(max_length=256)
    username = models.CharField(max_length=256, null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=64, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.IntegerField(choices=GENDER_VALID_CHOICES, default=1)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class UserProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="profile")
    designation = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return self.user.email
