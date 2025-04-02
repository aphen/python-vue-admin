from rest_framework import viewsets, status
from rest_framework.response import Response
from .department_models import Department
from .department_serializers import DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    
    def get_queryset(self):
        # 默认只返回顶级部门，避免重复显示
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            # 这些操作需要查询所有部门，以便能找到子部门
            return Department.objects.all().order_by('order', 'id')
        else:
            # list等操作只返回顶级部门，子部门通过嵌套序列化器返回
            return Department.objects.filter(parent__isnull=True).order_by('order', 'id')

    def create(self, request, *args, **kwargs):
        name = request.data.get('name')
        parent_id = request.data.get('parent')
        if Department.objects.filter(name=name, parent_id=parent_id).exists():
            return Response({"msg": "部门名称已存在"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        department = serializer.save()

        # 重新获取序列化数据，包含parent_name等信息
        response_serializer = self.get_serializer(department)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data.copy()
        name = data.get('name')
        parent_id = data.get('parent')
        if Department.objects.filter(name=name, parent_id=parent_id).exists():
            return Response({"msg": "部门名称已存在"}, status=status.HTTP_400_BAD_REQUEST)

        if 'parent' not in data:
            data['parent'] = None

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            def delete_department_recursive(dept):
                # 递归删除所有子部门
                for child in dept.children.all():
                    delete_department_recursive(child)
                dept.delete()
            
            delete_department_recursive(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response({"detail": "部门不存在或已被删除"}, status=status.HTTP_404_NOT_FOUND)