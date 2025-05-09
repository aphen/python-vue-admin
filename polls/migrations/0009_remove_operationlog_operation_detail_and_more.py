# Generated by Django 5.1.7 on 2025-04-02 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_operationlog'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operationlog',
            name='operation_detail',
        ),
        migrations.AddField(
            model_name='operationlog',
            name='request_method',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='请求方法'),
        ),
        migrations.AddField(
            model_name='operationlog',
            name='request_path',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='请求地址'),
        ),
        migrations.AddField(
            model_name='operationlog',
            name='response_code',
            field=models.IntegerField(blank=True, null=True, verbose_name='响应码'),
        ),
        migrations.AddField(
            model_name='operationlog',
            name='user_agent',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='操作浏览器'),
        ),
        migrations.AlterField(
            model_name='operationlog',
            name='operation_model',
            field=models.CharField(max_length=100, verbose_name='操作模块'),
        ),
    ]
