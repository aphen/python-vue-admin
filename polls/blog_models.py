from django.db import models
from django.contrib.auth.models import User
from .blog_tag_models import Tag

class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    summary = models.TextField(max_length=500, verbose_name='摘要')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='作者')
    tags = models.ManyToManyField(Tag, related_name='blog_posts', blank=True, verbose_name='标签')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'
    
    def __str__(self):
        return self.title