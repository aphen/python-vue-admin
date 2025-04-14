from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .todo_models import Todo
from .todo_serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def completed_todos(self, request):
        completed_todos = Todo.objects.filter(completed=True)
        page = self.paginate_queryset(completed_todos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(completed_todos, many=True)
        return Response(serializer.data)

    # 查询未完成的Todo
    @action(detail=False, methods=['get'])
    def uncompleted_todos(self, request):
        uncompleted_todos = Todo.objects.filter(completed=False)
        page = self.paginate_queryset(uncompleted_todos)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(uncompleted_todos, many=True)
        return Response(serializer.data)

    # 标记当前Todo为已完成
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        todo = self.get_object()
        todo.completed = True
        todo.save()
    # 清除所有已完成的Todo
    @action(detail=False, methods=['delete'])
    def clear_completed(self, request):
        completed_todos = Todo.objects.filter(completed=True)
        completed_todos.delete()
        return Response({'message': '已完成的Todo已清除'}, status=204)