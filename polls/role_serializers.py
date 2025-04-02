from rest_framework import serializers
from .role_models import Role
from django.contrib.auth.models import User

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'users', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class RoleDetailSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'users', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
    
    def get_users(self, obj):
        return [{
            'id': user.id,
            'username': user.username,
            'email': user.email
        } for user in obj.users.all()]