from rest_framework import serializers
from .blog_comment_models import BlogComment
from .operation_log_serializers import UserSerializer

class BlogCommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = BlogComment
        fields = ['id', 'post', 'author', 'author_id', 'content', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)