from rest_framework import serializers
from .department_models import Department

class SimpleDepartmentSerializer(serializers.ModelSerializer):
    full_path = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'parent', 'order', 'full_path']

    def get_full_path(self, obj):
        path = obj.name
        parent = obj.parent
        while parent:
            path = f"{parent.name}/{path}"
            parent = parent.parent
        return path

class DepartmentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent_name = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ['id', 'name', 'parent', 'parent_name', 'order', 'children', 'created_at', 'updated_at']

    def get_children(self, obj):
        children = Department.objects.filter(parent=obj).order_by('order', 'id')
        # 递归序列化子部门，这样可以获取所有层级的部门
        return DepartmentSerializer(children, many=True, context=self.context).data

    def get_parent_name(self, obj):
        return obj.parent.name if obj.parent else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # 构建完整的部门路径
        path = instance.name
        parent = instance.parent
        while parent:
            path = f"{parent.name}/{path}"
            parent = parent.parent
        data['full_path'] = path
        if instance.parent:
            data['parent'] = SimpleDepartmentSerializer(instance.parent).data
        return data