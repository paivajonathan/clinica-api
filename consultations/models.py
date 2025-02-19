from django.db import models
from django.utils.translation import gettext as _


class Consultation(models.Model):
    STATUS_CHOICES = (
        ("S", _("Scheduled")),
        ("F", _("Finished")),
        ("C", _("Canceled"))
    )
    
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    observations = models.CharField(max_length=200, default="")
    patient = models.ForeignKey("users.Patient", on_delete=models.RESTRICT, related_name="consultations")
    doctor = models.ForeignKey("users.Doctor", on_delete=models.RESTRICT, related_name="consultations")


class Attendance(models.Model):
    observations = models.TextField()
    consultation = models.ForeignKey(Consultation, on_delete=models.RESTRICT, related_name="attendances")
