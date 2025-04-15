from django.db import models
from django.conf import settings
from .blog_models import BlogPost

class BlogComment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = '博客评论'
        verbose_name_plural = '博客评论'

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'