# Generated by Django 4.0.4 on 2022-07-01 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_profile', '0002_alter_profile_bio_alter_profile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(auto_created=True, max_length=150),
        ),
    ]
