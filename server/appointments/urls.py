from django.urls import path
from .views import (
    DoctorListView,
    AppointmentListCreateView,
    AppointmentDetailView,
    AppointmentCancelView,
)

urlpatterns = [
    path("doctors/", DoctorListView.as_view(), name="doctor_list"),
    path("", AppointmentListCreateView.as_view(), name="appointment_list_create"),
    path("<int:pk>/", AppointmentDetailView.as_view(), name="appointment_detail"),
    path("<int:pk>/cancel/", AppointmentCancelView.as_view(), name="appointment_cancel"),
]