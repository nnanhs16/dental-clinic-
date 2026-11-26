from django.contrib import admin
from .models import MedicalRecord


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "doctor",
        "service_name",
        "examination_date",
        "follow_up_date",
    )

    list_filter = (
        "examination_date",
        "doctor",
    )

    search_fields = (
        "patient__full_name",
        "doctor__username",
        "service_name",
    )

    readonly_fields = ("created_at",)