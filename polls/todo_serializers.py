from rest_framework import serializers
from .todo_models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'content', 'completed', 'created_at')
        read_only_fields = ('created_at',)