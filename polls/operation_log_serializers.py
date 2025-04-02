from rest_framework import serializers
from .operation_log_models import OperationLog
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class OperationLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    operation_type_display = serializers.CharField(source='get_operation_type_display', read_only=True)
    
    class Meta:
        model = OperationLog
        fields = ['id', 'user', 'operation_type', 'operation_type_display', 'operation_model', 
                  'request_path', 'request_method', 'user_agent', 'response_code', 'ip_address', 'operation_time']
        read_only_fields = ['id', 'operation_time']