from rest_framework import serializers
from django.contrib.auth.models import User
from .blog_models import BlogPost
from .blog_tag_serializers import TagSerializer
from .blog_tag_models import Tag

class BlogAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class BlogPostListSerializer(serializers.ModelSerializer):
    author = BlogAuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'summary', 'author', 'tags', 'created_at']

class BlogPostDetailSerializer(serializers.ModelSerializer):
    author = BlogAuthorSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'summary', 'author', 'tags', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        validated_data['author'] = self.context['request'].user
        instance = super().create(validated_data)
        instance.tags.set(tags)
        return instance
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['tags'] = TagSerializer(instance.tags.all(), many=True).data
        return ret