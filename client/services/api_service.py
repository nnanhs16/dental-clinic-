
import requests

from client.config.settings import BASE_URL, API_TIMEOUT, API_ENDPOINTS


class APIService:
    def __init__(self):
        self.base_url = BASE_URL
        self.timeout = API_TIMEOUT
        self.access_token = None
        self.refresh_token = None
        self.session = requests.Session()

    # Lấy URL API
    def get_url(self, endpoint):
        return self.base_url + endpoint

    # Tạo headers
    def get_headers(self, authenticated=True):
        headers = {
            "Content-Type": "application/json"
        }

        if authenticated and self.access_token:
            headers["Authorization"] = (
                f"Bearer {self.access_token}"
            )

        return headers

    # Gửi request chung
    def request(self, method, endpoint, data=None, params=None,
                authenticated=True, retry=True):

        url = self.get_url(endpoint)

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=self.get_headers(authenticated),
                timeout=self.timeout
            )

            # Access Token hết hạn: thử refresh một lần
            if response.status_code == 401 and retry and self.refresh_token:
                if self.refresh_access_token():
                    return self.request(
                        method,
                        endpoint,
                        data=data,
                        params=params,
                        authenticated=authenticated,
                        retry=False
                    )

            if response.status_code == 204:
                return {
                    "success": True,
                    "data": None,
                    "message": "Thao tác thành công."
                }

            try:
                result = response.json()
            except ValueError:
                result = {"message": response.text}

            if response.ok:
                return {
                    "success": True,
                    "data": result,
                    "message": "Thành công."
                }

            return {
                "success": False,
                "data": result,
                "message": "Yêu cầu thất bại.",
                "status_code": response.status_code
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "data": None,
                "message": "Máy chủ phản hồi quá lâu."
            }

        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "data": None,
                "message": "Không thể kết nối máy chủ Django."
            }

        except requests.exceptions.RequestException as error:
            return {
                "success": False,
                "data": None,
                "message": str(error)
            }

    # Đăng nhập
    def login(self, username, password):
        result = self.request(
            "POST",
            API_ENDPOINTS["login"],
            data={
                "username": username,
                "password": password
            },
            authenticated=False
        )

        if result["success"]:
            token_data = result["data"]

            self.access_token = token_data.get("access")
            self.refresh_token = token_data.get("refresh")

        return result

    # Đăng ký
    def register(self, data):
        return self.request(
            "POST",
            API_ENDPOINTS["register"],
            data=data,
            authenticated=False
        )

    # Làm mới Access Token
    def refresh_access_token(self):
        if not self.refresh_token:
            return False

        result = self.request(
            "POST",
            API_ENDPOINTS["refresh"],
            data={"refresh": self.refresh_token},
            authenticated=False,
            retry=False
        )

        if result["success"]:
            self.access_token = result["data"].get("access")
            return bool(self.access_token)

        self.logout()
        return False

    # Lấy thông tin tài khoản hiện tại
    def get_current_user(self):
        return self.request(
            "GET",
            API_ENDPOINTS["current_user"]
        )

    # Lấy hồ sơ bệnh nhân
    def get_patient_profile(self):
        return self.request(
            "GET",
            API_ENDPOINTS["patient_profile"]
        )

    # Cập nhật hồ sơ bệnh nhân
    def update_patient_profile(self, data):
        return self.request(
            "PATCH",
            API_ENDPOINTS["patient_profile"],
            data=data
        )

    # Lấy danh sách bác sĩ
    def get_doctors(self):
        return self.request(
            "GET",
            API_ENDPOINTS["doctors"]
        )

    # Lấy danh sách dịch vụ
    def get_services(self, search=None, category=None):
        params = {}

        if search:
            params["search"] = search

        if category:
            params["category"] = category

        return self.request(
            "GET",
            API_ENDPOINTS["services"],
            params=params,
            authenticated=False
        )

    # Đặt lịch khám
    def create_appointment(self, data):
        return self.request(
            "POST",
            API_ENDPOINTS["appointments"],
            data=data
        )

    # Xem lịch hẹn
    def get_appointments(self):
        return self.request(
            "GET",
            API_ENDPOINTS["appointments"]
        )

    # Đổi lịch hẹn
    def update_appointment(self, appointment_id, data):
        endpoint = f"{API_ENDPOINTS['appointments']}{appointment_id}/"

        return self.request(
            "PATCH",
            endpoint,
            data=data
        )

    # Hủy lịch hẹn
    def cancel_appointment(self, appointment_id):
        endpoint = (
            f"{API_ENDPOINTS['appointments']}"
            f"{appointment_id}/cancel/"
        )

        return self.request(
            "POST",
            endpoint
        )

    # Xem lịch sử khám
    def get_medical_records(self):
        return self.request(
            "GET",
            API_ENDPOINTS["medical_records"]
        )

    # Xem chi tiết hồ sơ khám
    def get_medical_record_detail(self, record_id):
        endpoint = (
            f"{API_ENDPOINTS['medical_records']}"
            f"{record_id}/"
        )

        return self.request("GET", endpoint)

    # Xem đánh giá
    def get_reviews(self):
        return self.request(
            "GET",
            API_ENDPOINTS["reviews"]
        )

    # Gửi đánh giá
    def create_review(self, data):
        return self.request(
            "POST",
            API_ENDPOINTS["reviews"],
            data=data
        )

    # Sửa đánh giá
    def update_review(self, review_id, data):
        endpoint = f"{API_ENDPOINTS['reviews']}{review_id}/"

        return self.request(
            "PATCH",
            endpoint,
            data=data
        )

    # Xóa đánh giá
    def delete_review(self, review_id):
        endpoint = f"{API_ENDPOINTS['reviews']}{review_id}/"

        return self.request(
            "DELETE",
            endpoint
        )

    # Đăng xuất phía client
    def logout(self):
        self.access_token = None
        self.refresh_token = None
        self.session.cookies.clear()
