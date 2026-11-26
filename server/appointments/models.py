
from django.db import models
from django.conf import settings
from patients.models import Patient


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = "PENDING", "Chờ xác nhận"
        CONFIRMED = "CONFIRMED", "Đã xác nhận"
        CANCELLED = "CANCELLED", "Đã hủy"
        COMPLETED = "COMPLETED", "Đã hoàn thành"

    # Bệnh nhân đặt lịch
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Bệnh nhân"
    )

    # Bác sĩ phụ trách
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="doctor_appointments",
        limit_choices_to={"role": "DOCTOR"},
        verbose_name="Bác sĩ"
    )

    # Dịch vụ bệnh nhân lựa chọn
    service_name = models.CharField(
        max_length=150,
        verbose_name="Dịch vụ"
    )

    # Ngày và giờ khám
    appointment_datetime = models.DateTimeField(
        verbose_name="Ngày giờ khám"
    )

    # Lý do khám
    reason = models.TextField(
        blank=True,
        verbose_name="Lý do khám"
    )

    # Trạng thái lịch hẹn
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Trạng thái"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật"
    )

    class Meta:
        db_table = "appointments"
        verbose_name = "Lịch hẹn"
        verbose_name_plural = "Lịch hẹn"
        ordering = ["-appointment_datetime"]

    def __str__(self):
        return (
            f"{self.patient.full_name} - "
            f"{self.appointment_datetime}"
        )
