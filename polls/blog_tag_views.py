from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .blog_tag_models import Tag
from .blog_tag_serializers import TagSerializer

class BlogTagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.annotate(blog_posts_count=Count('blog_posts'))
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['GET'])
    def popular(self, request):
        """获取最热门的标签（按关联文章数量排序）"""
        tags = self.get_queryset().order_by('-blog_posts_count')[:10]
        serializer = self.get_serializer(tags, many=True)
        return Response(serializer.data)