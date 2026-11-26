
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError

from .models import Appointment
from .serializers import (
    AppointmentSerializer,
    DoctorSerializer,
)

User = get_user_model()


# API lấy danh sách bác sĩ
class DoctorListView(generics.ListAPIView):

    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(
            role=User.Role.DOCTOR,
            is_active=True
        ).order_by("id")


# API xem danh sách và đặt lịch khám
class AppointmentListCreateView(generics.ListCreateAPIView):

    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != User.Role.PATIENT:
            return Appointment.objects.none()

        return Appointment.objects.filter(
            patient__user=self.request.user
        ).select_related(
            "patient",
            "doctor"
        )

    def perform_create(self, serializer):
        if self.request.user.role != User.Role.PATIENT:
            raise ValidationError(
                "Chỉ bệnh nhân mới được đặt lịch khám."
            )

        try:
            patient = self.request.user.patient_profile
        except Exception:
            raise ValidationError(
                "Tài khoản chưa có hồ sơ bệnh nhân."
            )

        serializer.save(patient=patient)


# API xem chi tiết, đổi lịch và hủy lịch
class AppointmentDetailView(generics.RetrieveUpdateAPIView):

    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch", "head", "options"]

    def get_queryset(self):
        return Appointment.objects.filter(
            patient__user=self.request.user
        ).select_related(
            "patient",
            "doctor"
        )

    def perform_update(self, serializer):
        appointment = self.get_object()

        if appointment.status != Appointment.Status.PENDING:
            raise ValidationError(
                "Chỉ lịch hẹn đang chờ xác nhận mới được thay đổi."
            )

        serializer.save()


# API hủy lịch
class AppointmentCancelView(generics.GenericAPIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            appointment = Appointment.objects.get(
                pk=pk,
                patient__user=request.user
            )
        except Appointment.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound("Không tìm thấy lịch hẹn.")

        if appointment.status not in [
            Appointment.Status.PENDING,
            Appointment.Status.CONFIRMED,
        ]:
            raise ValidationError(
                "Lịch hẹn này không thể hủy."
            )

        appointment.status = Appointment.Status.CANCELLED
        appointment.save(update_fields=["status", "updated_at"])

        return Response({
            "message": "Hủy lịch hẹn thành công."
        })
