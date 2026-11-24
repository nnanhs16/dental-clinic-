
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Bệnh nhân"
        RECEPTIONIST = "RECEPTIONIST", "Lễ tân"
        NURSE = "NURSE", "Điều dưỡng"
        DENTAL_ASSISTANT = "DENTAL_ASSISTANT", "Phụ tá nha khoa"
        DOCTOR = "DOCTOR", "Bác sĩ"
        OWNER = "OWNER", "Chủ phòng khám"
        MANAGER = "MANAGER", "Quản lý"
        ADMIN_HR = "ADMIN_HR", "Quản trị nhân sự"
        ACCOUNTANT = "ACCOUNTANT", "Kế toán"
        HR = "HR", "Nhân sự"
        SYSTEM_ADMIN = "SYSTEM_ADMIN", "Quản trị hệ thống"

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.PATIENT,
        verbose_name="Vai trò"
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Số điện thoại"
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
        db_table = "users"
        verbose_name = "Tài khoản"
        verbose_name_plural = "Tài khoản"

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
