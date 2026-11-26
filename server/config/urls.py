from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/accounts/", include("accounts.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/appointments/", include("appointments.urls")),
    path("api/services/", include("services.urls")),
    path("api/medical-records/", include("medical_records.urls")),
    path("api/reviews/", include("reviews.urls")),
]