from rest_framework import serializers
from .role_models import Role
from django.contrib.auth.models import User, Permission

class PermissionSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ('id', 'name', 'codename', 'content_type')

    def get_content_type(self, obj):
        return {
            'app_label': obj.content_type.app_label,
            'model': obj.content_type.model
        }

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'users', 'permissions', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class RoleDetailSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'users', 'permissions', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
    
    def get_users(self, obj):
        return [{
            'id': user.id,
            'username': user.username,
            'email': user.email
        } for user in obj.users.all()]