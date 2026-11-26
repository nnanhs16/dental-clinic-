from django.db import models


class Service(models.Model):

    class Category(models.TextChoices):
        GENERAL = "GENERAL", "Khám tổng quát"
        CLEANING = "CLEANING", "Vệ sinh răng miệng"
        COSMETIC = "COSMETIC", "Thẩm mỹ nha khoa"
        RESTORATION = "RESTORATION", "Phục hình răng"
        ORTHODONTICS = "ORTHODONTICS", "Chỉnh nha"
        SURGERY = "SURGERY", "Phẫu thuật nha khoa"

    name = models.CharField(
        max_length=150,
        verbose_name="Tên dịch vụ"
    )

    category = models.CharField(
        max_length=30,
        choices=Category.choices,
        default=Category.GENERAL,
        verbose_name="Danh mục"
    )

    description = models.TextField(
        blank=True,
        verbose_name="Mô tả"
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        verbose_name="Giá dịch vụ"
    )

    duration = models.PositiveIntegerField(
        default=30,
        verbose_name="Thời gian thực hiện (phút)"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Đang cung cấp"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "services"
        verbose_name = "Dịch vụ"
        verbose_name_plural = "Dịch vụ"
        ordering = ["name"]

    def __str__(self):
        return self.name