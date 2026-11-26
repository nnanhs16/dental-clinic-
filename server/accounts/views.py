from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    UserSerializer,
    PatientRegisterSerializer,
)


# API lấy thông tin tài khoản đang đăng nhập
class CurrentUserView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# API đăng ký tài khoản bệnh nhân
class PatientRegisterView(generics.CreateAPIView):

    serializer_class = PatientRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "Đăng ký tài khoản thành công.",
                "username": user.username,
                "role": user.role,
            },
            status=status.HTTP_201_CREATED
        )
