from django.db import models
from patients.models import Patient
from accounts.models import User
from appointments.models import Appointment


class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_records",
        verbose_name="Bệnh nhân"
    )

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="medical_record",
        verbose_name="Lịch hẹn"
    )

    doctor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={"role": "DOCTOR"},
        verbose_name="Bác sĩ"
    )

    examination_date = models.DateTimeField(
        verbose_name="Ngày khám"
    )

    service_name = models.CharField(
        max_length=150,
        verbose_name="Dịch vụ"
    )

    diagnosis = models.TextField(
        verbose_name="Chẩn đoán"
    )

    result = models.TextField(
        blank=True,
        verbose_name="Kết quả khám"
    )

    treatment = models.TextField(
        blank=True,
        verbose_name="Hướng dẫn điều trị"
    )

    follow_up_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày tái khám"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "medical_records"
        verbose_name = "Hồ sơ khám bệnh"
        verbose_name_plural = "Hồ sơ khám bệnh"
        ordering = ["-examination_date"]

    def __str__(self):
        return f"{self.patient.full_name} - {self.examination_date}"