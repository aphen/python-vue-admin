from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from .role_models import Role
from .role_serializers import RoleSerializer, RoleDetailSerializer

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RoleDetailSerializer
        return RoleSerializer

    @action(detail=True, methods=['post'])
    def assign_users(self, request, pk=None):
        role = self.get_object()
        user_ids = request.data.get('user_ids', [])
        
        try:
            users = User.objects.filter(id__in=user_ids)
            role.users.set(users)
            return Response({'message': '用户分配成功'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_users(self, request, pk=None):
        role = self.get_object()
        user_ids = request.data.get('user_ids', [])
        
        try:
            users = User.objects.filter(id__in=user_ids)
            role.users.remove(*users)
            return Response({'message': '用户移除成功'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def permissions(self, request):
        content_types = ContentType.objects.all()
        permissions = []
        for ct in content_types:
            perms = Permission.objects.filter(content_type=ct)
            for perm in perms:
                permissions.append({
                    'id': perm.id,
                    'name': perm.name,
                    'codename': perm.codename,
                    'content_type': {
                        'app_label': ct.app_label,
                        'model': ct.model
                    }
                })
        return Response(permissions)

    @action(detail=True, methods=['post'])
    def assign_permissions(self, request, pk=None):
        role = self.get_object()
        permission_ids = request.data.get('permission_ids', [])
        
        try:
            permissions = Permission.objects.filter(id__in=permission_ids)
            role.permissions.set(permissions)
            return Response({'message': '权限分配成功'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    # 根据角色ids查询权限
    @action(detail=False, methods=['get'])
    def permissions_by_role_ids(self, request):
        role_ids = request.query_params.get('role_ids', '')
        if not role_ids:
            return Response([], status=status.HTTP_200_OK)
        
        role_ids = [int(id) for id in role_ids.split(',')]
        roles = Role.objects.filter(id__in=role_ids)
        
        # 获取所有角色关联的权限
        all_permissions = set()
        for role in roles:
            all_permissions.update(role.permissions.all())
        
        # 使用PermissionSerializer序列化权限数据
        from .role_serializers import PermissionSerializer
        serializer = PermissionSerializer(list(all_permissions), many=True)
        return Response(serializer.data)