# Generated by Django 4.0.4 on 2022-07-01 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0017_alter_organisationscomment_author_alter_ratings_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisations',
            name='slug',
            field=models.SlugField(auto_created=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='tours',
            name='slug',
            field=models.SlugField(max_length=150, unique=True),
        ),
    ]