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
    status = models.CharField(max_length=1, default="S", choices=STATUS_CHOICES)
    observations = models.CharField(max_length=200, default="Sem observações")
    patient = models.ForeignKey("users.Patient", on_delete=models.RESTRICT, related_name="consultations")
    doctor = models.ForeignKey("users.Doctor", on_delete=models.RESTRICT, related_name="consultations")
    
    def __str__(self):
        return f"{self.patient.user.first_name} - {self.doctor.user.first_name} - {self.date} - {self.time} - {self.status} - {self.observations}"
    
    class Meta:
        db_table = "consultations"
        ordering = ["-id"]
        verbose_name = _("Consultation")
        verbose_name_plural = _("Consultations")


class Attendance(models.Model):
    observations = models.TextField()
    consultation = models.ForeignKey(Consultation, on_delete=models.RESTRICT, related_name="attendances")

    def __str__(self):
        return f"{self.observations} - {self.consultation}"

    class Meta:
        db_table = "attendances"
        ordering = ["-id"]
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")
