
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CurrentUserView, PatientRegisterView


urlpatterns = [
    # Đăng ký bệnh nhân
    path(
        "register/",
        PatientRegisterView.as_view(),
        name="patient_register"
    ),

    # Đăng nhập lấy JWT
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),

    # Làm mới JWT
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),

    # Lấy thông tin tài khoản hiện tại
    path(
        "me/",
        CurrentUserView.as_view(),
        name="current_user"
    ),
]
