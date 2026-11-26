from django.urls import path
from .views import MedicalRecordListView, MedicalRecordDetailView

urlpatterns = [
    path("", MedicalRecordListView.as_view(), name="medical_record_list"),
    path("<int:pk>/", MedicalRecordDetailView.as_view(), name="medical_record_detail"),
]