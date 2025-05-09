# Generated by Django 5.1.7

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0007_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operation_type', models.CharField(choices=[('CREATE', '创建'), ('UPDATE', '更新'), ('DELETE', '删除'), ('LOGIN', '登录'), ('LOGOUT', '登出'), ('OTHER', '其他')], max_length=20, verbose_name='操作类型')),
                ('operation_model', models.CharField(max_length=100, verbose_name='操作模型')),
                ('operation_detail', models.TextField(verbose_name='操作详情')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('operation_time', models.DateTimeField(auto_now_add=True, verbose_name='操作时间')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='operation_logs', to=settings.AUTH_USER_MODEL, verbose_name='操作用户')),
            ],
            options={
                'verbose_name': '操作日志',
                'verbose_name_plural': '操作日志',
                'ordering': ['-operation_time'],
            },
        ),
    ]