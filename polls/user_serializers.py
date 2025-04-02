from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.serializers import SerializerMethodField
from .role_models import Role
from .role_serializers import RoleSerializer
from .department_models import Department
from .department_serializers import DepartmentSerializer, SimpleDepartmentSerializer

class UserListSerializer(serializers.ModelSerializer):
    date_joined = SerializerMethodField()
    roles = RoleSerializer(many=True, read_only=True)
    department = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser', 'date_joined', 'roles', 'department')
    
    def get_date_joined(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d %H:%M:%S') if obj.date_joined else None

    def get_department(self, obj):
        try:
            if hasattr(obj, 'profile') and obj.profile.department:
                return SimpleDepartmentSerializer(obj.profile.department).data
        except:
            pass
        return None

class UserDetailSerializer(serializers.ModelSerializer):
    date_joined = SerializerMethodField()
    last_login = SerializerMethodField()
    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all())
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), allow_null=True, required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login', 'roles', 'department')
        read_only_fields = ('date_joined', 'last_login')
    
    def get_date_joined(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d %H:%M:%S') if obj.date_joined else None

    def get_department(self, obj):
        try:
            if hasattr(obj, 'profile') and obj.profile.department:
                return SimpleDepartmentSerializer(obj.profile.department).data
        except:
            pass
        return None
    
    def get_last_login(self, obj):
        return obj.last_login.strftime('%Y-%m-%d %H:%M:%S') if obj.last_login else None

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', None)
        department = validated_data.pop('department', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 如果用户有profile，更新department；否则创建新的profile
        if hasattr(instance, 'profile'):
            instance.profile.department = department
            instance.profile.save()
        elif department is not None:
            # 如果用户没有profile但提供了department，创建新的profile
            from .models import UserProfile
            UserProfile.objects.create(user=instance, department=department)

        if roles_data is not None:
            instance.roles.set(roles_data)
        return instance
class CreateUserSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all(), required=False)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), allow_null=True, required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'roles', 'department')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        department = validated_data.pop('department', None)
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data.get('password', '123456'))
        user.save()
        
        # 创建用户配置并关联部门
        from .models import UserProfile
        UserProfile.objects.create(user=user, department=department)
        
        # 设置用户角色
        if roles_data:
            user.roles.set(roles_data)
            
        return user