
from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    """
    Kiểm tra người dùng có vai trò được phép truy cập API hay không.

    Cách sử dụng trong View:
        allowed_roles = ["DOCTOR", "NURSE"]
        permission_classes = [RolePermission]
    """

    message = "Bạn không có quyền thực hiện chức năng này."

    def has_permission(self, request, view):
        user = request.user

        # Chưa đăng nhập
        if not user or not user.is_authenticated:
            return False

        # Quản trị hệ thống được phép truy cập
        if user.is_superuser or user.role == "SYSTEM_ADMIN":
            return True

        # Lấy danh sách vai trò được phép từ View
        allowed_roles = getattr(view, "allowed_roles", [])

        # Không khai báo vai trò thì mặc định từ chối
        if not allowed_roles:
            return False

        return user.role in allowed_roles


class IsSystemAdmin(BasePermission):
    """
    Chỉ cho phép quản trị hệ thống truy cập.
    """

    message = "Chỉ quản trị hệ thống mới được thực hiện chức năng này."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and (
                user.is_superuser
                or user.role == "SYSTEM_ADMIN"
            )
        )


class IsSelfOrSystemAdmin(BasePermission):
    """
    Người dùng chỉ được xem/chỉnh sửa dữ liệu của chính mình.
    Quản trị hệ thống được phép truy cập.
    """

    message = "Bạn không có quyền truy cập dữ liệu của người khác."

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.is_superuser or user.role == "SYSTEM_ADMIN":
            return True

        # Chỉ cho phép truy cập đối tượng thuộc chính tài khoản
        return obj.pk == user.pk
