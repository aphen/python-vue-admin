from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='标签名')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tags', verbose_name='创建者')
    
    class Meta:
        ordering = ['name']
        verbose_name = '标签'
        verbose_name_plural = '标签'
    
    def __str__(self):
        return self.name