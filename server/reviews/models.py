from django.db import models
from patients.models import Patient
from services.models import Service


class Review(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Bệnh nhân"
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="reviews",
        verbose_name="Dịch vụ"
    )

    rating = models.PositiveSmallIntegerField(
        verbose_name="Số sao"
    )

    comment = models.TextField(
        blank=True,
        verbose_name="Nội dung đánh giá"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reviews"
        verbose_name = "Đánh giá dịch vụ"
        verbose_name_plural = "Đánh giá dịch vụ"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["patient", "service"],
                name="unique_patient_service_review"
            ),
            models.CheckConstraint(
                check=models.Q(rating__gte=1, rating__lte=5),
                name="review_rating_between_1_and_5"
            ),
        ]

    def __str__(self):
        return f"{self.patient.full_name} - {self.service.name}"