
from django.db import models
from django.conf import settings


class Patient(models.Model):

    class Gender(models.TextChoices):
        MALE = "MALE", "Nam"
        FEMALE = "FEMALE", "Nữ"
        OTHER = "OTHER", "Khác"

    # Liên kết một hồ sơ với một tài khoản
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
        verbose_name="Tài khoản"
    )

    patient_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Mã bệnh nhân"
    )

    full_name = models.CharField(
        max_length=100,
        verbose_name="Họ và tên"
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Ngày sinh"
    )

    gender = models.CharField(
        max_length=10,
        choices=Gender.choices,
        blank=True,
        verbose_name="Giới tính"
    )

    address = models.TextField(
        blank=True,
        verbose_name="Địa chỉ"
    )

    occupation = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nghề nghiệp"
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
        db_table = "patients"
        verbose_name = "Bệnh nhân"
        verbose_name_plural = "Bệnh nhân"

    def __str__(self):
        return f"{self.patient_code} - {self.full_name}"
