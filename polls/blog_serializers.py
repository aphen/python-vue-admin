from rest_framework import serializers
from django.contrib.auth.models import User
from .blog_models import BlogPost

class BlogAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class BlogPostListSerializer(serializers.ModelSerializer):
    author = BlogAuthorSerializer(read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'summary', 'author', 'created_at']

class BlogPostDetailSerializer(serializers.ModelSerializer):
    author = BlogAuthorSerializer(read_only=True)
    
    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'summary', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)