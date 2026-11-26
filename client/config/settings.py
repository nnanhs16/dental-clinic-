
# Địa chỉ Django Backend
BASE_URL = "http://127.0.0.1:8000"

# Thời gian chờ khi gọi API (giây)
API_TIMEOUT = 15

# Các đường dẫn API
API_ENDPOINTS = {
    "register": "/api/accounts/register/",
    "login": "/api/accounts/token/",
    "refresh": "/api/accounts/token/refresh/",
    "current_user": "/api/accounts/me/",
    "patient_profile": "/api/patients/profile/",
    "doctors": "/api/appointments/doctors/",
    "appointments": "/api/appointments/",
    "services": "/api/services/",
    "medical_records": "/api/medical-records/",
    "reviews": "/api/reviews/",
}
