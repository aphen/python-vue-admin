from django.db import models
from django.contrib.auth.models import User

class OperationLog(models.Model):
    OPERATION_TYPES = (
        ('CREATE', '创建'),
        ('UPDATE', '更新'),
        ('DELETE', '删除'),
        ('LOGIN', '登录'),
        ('LOGOUT', '登出'),
        ('OTHER', '其他'),
    )
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='operation_logs', verbose_name='操作用户')
    operation_type = models.CharField(max_length=20, choices=OPERATION_TYPES, verbose_name='操作类型')
    operation_model = models.CharField(max_length=100, verbose_name='操作模块')
    request_path = models.CharField(max_length=255, null=True, blank=True, verbose_name='请求地址')
    request_method = models.CharField(max_length=10, null=True, blank=True, verbose_name='请求方法')
    user_agent = models.CharField(max_length=255, null=True, blank=True, verbose_name='操作浏览器')
    response_code = models.IntegerField(null=True, blank=True, verbose_name='响应码')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP地址')
    operation_time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    
    class Meta:
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ['-operation_time']
    
    def __str__(self):
        return f"{self.get_operation_type_display()} - {self.operation_model} - {self.user}"