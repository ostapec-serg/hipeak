# Generated by Django 4.0.4 on 2022-05-17 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_blog', '0006_news_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
