from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .blog_comment_models import BlogComment
from .blog_comment_serializers import BlogCommentSerializer

class BlogCommentViewSet(viewsets.ModelViewSet):
    queryset = BlogComment.objects.all()
    serializer_class = BlogCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id', None)
        if post_id is not None:
            return BlogComment.objects.filter(post_id=post_id)
        return BlogComment.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != request.user and not request.user.is_staff:
            return Response(
                {"detail": "您没有权限删除此评论"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)