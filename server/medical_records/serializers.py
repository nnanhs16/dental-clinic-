from rest_framework import serializers
from .models import MedicalRecord


class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()
    patient_name = serializers.CharField(
        source="patient.full_name",
        read_only=True
    )

    class Meta:
        model = MedicalRecord
        fields = [
            "id",
            "patient",
            "patient_name",
            "appointment",
            "doctor",
            "doctor_name",
            "examination_date",
            "service_name",
            "diagnosis",
            "result",
            "treatment",
            "follow_up_date",
            "created_at",
        ]

        read_only_fields = fields

    def get_doctor_name(self, obj):
        return obj.doctor.get_full_name() or obj.doctor.username