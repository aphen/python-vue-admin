from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .operation_log_models import OperationLog
from .operation_log_serializers import OperationLogSerializer

class OperationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    操作日志视图集，只提供只读操作
    """
    queryset = OperationLog.objects.all()
    serializer_class = OperationLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['operation_type', 'operation_model', 'user']
    search_fields = ['operation_detail']
    ordering_fields = ['operation_time']
    ordering = ['-operation_time']