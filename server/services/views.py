from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Service
from .serializers import ServiceSerializer


class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Service.objects.filter(is_active=True)

        # Tìm kiếm theo tên dịch vụ
        keyword = self.request.query_params.get("search")

        if keyword:
            queryset = queryset.filter(name__icontains=keyword)

        # Lọc theo danh mục
        category = self.request.query_params.get("category")

        if category:
            queryset = queryset.filter(category=category)

        return queryset