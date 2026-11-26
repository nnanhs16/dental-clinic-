from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import MedicalRecord
from .serializers import MedicalRecordSerializer


class MedicalRecordListView(generics.ListAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "PATIENT":
            raise PermissionDenied(
                "Chỉ bệnh nhân mới được xem lịch sử khám tại API này."
            )

        return MedicalRecord.objects.filter(
            patient__user=self.request.user
        ).select_related("patient", "doctor", "appointment")


class MedicalRecordDetailView(generics.RetrieveAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "PATIENT":
            raise PermissionDenied(
                "Chỉ bệnh nhân mới được xem hồ sơ khám."
            )

        return MedicalRecord.objects.filter(
            patient__user=self.request.user
        ).select_related("patient", "doctor", "appointment")