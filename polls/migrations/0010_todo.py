# Generated by Django 5.2 on 2025-04-08 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_remove_operationlog_operation_detail_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=100)),
                ('compoleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
