from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
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