# Generated by Django 4.0.4 on 2022-07-01 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment_stores', '0007_equipmentstores_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentstores',
            name='slug',
            field=models.SlugField(max_length=150, unique=True),
        ),
    ]