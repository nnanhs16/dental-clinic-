from rest_framework import serializers
from .models import Review
from medical_records.models import MedicalRecord


class ReviewSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(
        source="service.name",
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "service",
            "service_name",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        request = self.context.get("request")

        if request and request.user.role != "PATIENT":
            raise serializers.ValidationError(
                "Chỉ bệnh nhân mới được đánh giá dịch vụ."
            )

        service = attrs.get(
            "service",
            getattr(self.instance, "service", None)
        )

        if request and service:
            try:
                patient = request.user.patient_profile
            except Exception:
                raise serializers.ValidationError(
                    "Tài khoản chưa có hồ sơ bệnh nhân."
                )

            # Chỉ cho đánh giá dịch vụ đã có hồ sơ khám tương ứng
            has_used_service = MedicalRecord.objects.filter(
                patient=patient,
                service_name=service.name
            ).exists()

            if not has_used_service:
                raise serializers.ValidationError({
                    "service": "Bạn cần sử dụng dịch vụ trước khi đánh giá."
                })

        return attrs