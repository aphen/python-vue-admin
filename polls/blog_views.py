from rest_framework import viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .blog_models import BlogPost
from .blog_serializers import BlogPostListSerializer, BlogPostDetailSerializer

class BlogPostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BlogPostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = BlogPostPagination
    
    def get_queryset(self):
        return BlogPost.objects.select_related('author').all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BlogPostListSerializer
        return BlogPostDetailSerializer