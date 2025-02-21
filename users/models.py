from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from .manager import CustomUserManager


class User(AbstractUser):
    role = models.CharField(max_length=1)
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.get_full_name()}"
    
    class Meta:
        db_table = "users"
        ordering = ["-id"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")


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

    def __str__(self):
        return f"{self.user.get_full_name()}"

    class Meta:
        db_table = "patients"
        ordering = ["-id"]
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")


class Specialty(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description

    class Meta:
        db_table = "specialties"
        ordering = ["-id"]
        verbose_name = _("Specialty")
        verbose_name_plural = _("Specialties")


class Doctor(models.Model):
    code = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    specialty = models.ForeignKey("users.Specialty", on_delete=models.RESTRICT, related_name="doctors")
    user = models.OneToOneField("users.User", on_delete=models.RESTRICT, related_name="doctor")
    
    def __str__(self):
        return f"{self.user.get_full_name()}"
    
    class Meta:
        db_table = "doctors"
        ordering = ["-id"]
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")
