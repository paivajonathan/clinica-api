from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .manager import CustomUserManager


class User(AbstractUser):
    role = models.CharField(max_length=1)
    
    objects = CustomUserManager()


class Patient(models.Model):
    GENDER_CHOICES = (
        ("M", _("Masculine")),
        ("F", _("Feminine"))
    )
    
    birth_date = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=200)
    user = models.OneToOneField("users.User", on_delete=models.RESTRICT, related_name="patient")


class Specialty(models.Model):
    description = models.CharField(max_length=200)


class Doctor(models.Model):
    code = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    specialty = models.ForeignKey("users.Specialty", on_delete=models.RESTRICT, related_name="doctors")
    user = models.OneToOneField("users.User", on_delete=models.RESTRICT, related_name="doctor")