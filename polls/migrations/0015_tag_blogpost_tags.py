from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('polls', '0014_blogcomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='标签名')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_tags', to='auth.user', verbose_name='创建者')),
            ],
            options={
                'verbose_name': '标签',
                'verbose_name_plural': '标签',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='blog_posts', to='polls.tag', verbose_name='标签'),
        ),
    ]