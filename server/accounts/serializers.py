
import uuid

from django.db import transaction
from rest_framework import serializers

from .models import User
from patients.models import Patient


# ==================================================
# 1. SERIALIZER THÔNG TIN TÀI KHOẢN
# ==================================================

class UserSerializer(serializers.ModelSerializer):

    role_display = serializers.CharField(
        source="get_role_display",
        read_only=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "role_display",
            "phone_number",
        ]


# ==================================================
# 2. SERIALIZER ĐĂNG KÝ TÀI KHOẢN BỆNH NHÂN
# ==================================================

class PatientRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={"input_type": "password"}
    )

    full_name = serializers.CharField(
        max_length=100
    )

    date_of_birth = serializers.DateField(
        required=False,
        allow_null=True
    )

    gender = serializers.ChoiceField(
        choices=Patient.Gender.choices,
        required=False,
        allow_blank=True
    )

    address = serializers.CharField(
        required=False,
        allow_blank=True
    )

    occupation = serializers.CharField(
        required=False,
        allow_blank=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "phone_number",
            "full_name",
            "date_of_birth",
            "gender",
            "address",
            "occupation",
        ]

    # Kiểm tra email đã tồn tại chưa
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Email này đã được sử dụng."
            )

        return value

    # Tạo tài khoản và hồ sơ bệnh nhân
    @transaction.atomic
    def create(self, validated_data):

        # Tách thông tin hồ sơ bệnh nhân
        full_name = validated_data.pop("full_name")

        date_of_birth = validated_data.pop(
            "date_of_birth", None
        )

        gender = validated_data.pop("gender", "")

        address = validated_data.pop("address", "")

        occupation = validated_data.pop("occupation", "")

        # Tách mật khẩu để mã hóa
        password = validated_data.pop("password")

        # Tạo tài khoản người dùng
        user = User(**validated_data)

        user.role = User.Role.PATIENT

        user.set_password(password)

        user.save()

        # Sinh mã bệnh nhân tự động
        patient_code = "BN" + uuid.uuid4().hex[:10].upper()

        # Tạo hồ sơ bệnh nhân liên kết với tài khoản
        Patient.objects.create(
            user=user,
            patient_code=patient_code,
            full_name=full_name,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            occupation=occupation,
        )

        return user
