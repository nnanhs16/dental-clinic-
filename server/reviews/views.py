from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from .models import Review
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "PATIENT":
            raise PermissionDenied(
                "Chỉ bệnh nhân mới được xem đánh giá của mình."
            )

        return Review.objects.filter(
            patient__user=self.request.user
        ).select_related("patient", "service")

    def perform_create(self, serializer):
        if self.request.user.role != "PATIENT":
            raise PermissionDenied(
                "Chỉ bệnh nhân mới được gửi đánh giá."
            )

        serializer.save(patient=self.request.user.patient_profile)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role != "PATIENT":
            raise PermissionDenied(
                "Chỉ bệnh nhân mới được thao tác với đánh giá."
            )

        return Review.objects.filter(
            patient__user=self.request.user
        ).select_related("patient", "service")