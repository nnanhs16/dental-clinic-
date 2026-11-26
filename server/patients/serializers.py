
from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Patient

User = get_user_model()


class PatientProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(source="user.email")
    phone_number = serializers.CharField(
        source="user.phone_number",
        required=False,
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = Patient
        fields = [
            "id",
            "patient_code",
            "full_name",
            "date_of_birth",
            "gender",
            "address",
            "occupation",
            "email",
            "phone_number",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "patient_code",
            "created_at",
            "updated_at",
        ]

    def validate_email(self, value):
        current_user = self.instance.user

        if User.objects.filter(
            email__iexact=value
        ).exclude(pk=current_user.pk).exists():
            raise serializers.ValidationError(
                "Email này đã được sử dụng."
            )

        return value

    @transaction.atomic
    def update(self, instance, validated_data):

        user_data = validated_data.pop("user", {})

        # Cập nhật thông tin tài khoản
        user = instance.user

        if "email" in user_data:
            user.email = user_data["email"]

        if "phone_number" in user_data:
            user.phone_number = user_data["phone_number"]

        user.save()

        # Cập nhật thông tin hồ sơ bệnh nhân
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
