# Generated by Django 4.0.3 on 2022-05-06 14:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news_blog', '0003_rename_news_text_news_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=300)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('moderate_status', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 'Ok'), (2, 'Fine'), (3, 'Good'), (4, 'Nice'), (5, 'Amazing')], null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='news',
            name='readers',
        ),
        migrations.AddField(
            model_name='news',
            name='bookmark',
            field=models.ManyToManyField(related_name='bookmark_in', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='news',
            name='comment',
            field=models.ManyToManyField(related_name='comment_news', through='news_blog.Comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='news',
            name='like',
            field=models.ManyToManyField(related_name='liked_news', through='news_blog.Likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='news',
            name='rating',
            field=models.ManyToManyField(related_name='news_rating', through='news_blog.Ratings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='news',
            name='description',
            field=models.TextField(verbose_name='news_description'),
        ),
        migrations.AlterField(
            model_name='news',
            name='name',
            field=models.CharField(max_length=250, verbose_name='news_name'),
        ),
        migrations.DeleteModel(
            name='UserNewsRelated',
        ),
        migrations.AddField(
            model_name='ratings',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_blog.news'),
        ),
        migrations.AddField(
            model_name='ratings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='likes',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_blog.news'),
        ),
        migrations.AddField(
            model_name='likes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='news_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='news_blog.news'),
        ),
        migrations.AddField(
            model_name='bookmarks',
            name='news_bookmark',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news_blog.news'),
        ),
        migrations.AddField(
            model_name='bookmarks',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
