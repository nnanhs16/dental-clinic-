
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from .models import Patient
from .serializers import PatientProfileSerializer


class PatientProfileView(generics.RetrieveUpdateAPIView):

    serializer_class = PatientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):

        user = self.request.user

        try:
            return Patient.objects.get(user=user)
        except Patient.DoesNotExist:
            raise NotFound(
                "Không tìm thấy hồ sơ bệnh nhân."
            )
