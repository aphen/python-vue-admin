from rest_framework import serializers
from .blog_tag_models import Tag
from .operation_log_serializers import UserSerializer

class TagSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    blog_posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'created_by', 'created_at', 'blog_posts_count']

    def get_blog_posts_count(self, obj):
        return obj.blog_posts.count()

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)