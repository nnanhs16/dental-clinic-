
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Appointment

User = get_user_model()


# Serializer danh sách bác sĩ
class DoctorSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "email",
            "phone_number",
        ]

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


# Serializer lịch hẹn
class AppointmentSerializer(serializers.ModelSerializer):

    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = [
            "id",
            "doctor",
            "doctor_name",
            "service_name",
            "appointment_datetime",
            "reason",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "doctor_name",
            "status",
            "created_at",
            "updated_at",
        ]

    def get_doctor_name(self, obj):
        return obj.doctor.get_full_name() or obj.doctor.username

    def validate_doctor(self, value):
        if value.role != User.Role.DOCTOR:
            raise serializers.ValidationError(
                "Tài khoản được chọn không phải bác sĩ."
            )

        if not value.is_active:
            raise serializers.ValidationError(
                "Tài khoản bác sĩ hiện không hoạt động."
            )

        return value

    def validate_appointment_datetime(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Thời gian khám phải ở tương lai."
            )

        return value

    def validate(self, attrs):
        doctor = attrs.get(
            "doctor",
            getattr(self.instance, "doctor", None)
        )

        appointment_datetime = attrs.get(
            "appointment_datetime",
            getattr(self.instance, "appointment_datetime", None)
        )

        if doctor and appointment_datetime:
            conflicting = Appointment.objects.filter(
                doctor=doctor,
                appointment_datetime=appointment_datetime,
                status__in=[
                    Appointment.Status.PENDING,
                    Appointment.Status.CONFIRMED,
                ]
            )

            if self.instance:
                conflicting = conflicting.exclude(
                    pk=self.instance.pk
                )

            if conflicting.exists():
                raise serializers.ValidationError(
                    "Bác sĩ đã có lịch hẹn vào thời gian này."
                )

        return attrs
