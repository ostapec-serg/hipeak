# Generated by Django 4.0.4 on 2022-06-28 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment_stores', '0006_alter_equipmentstores_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipmentstores',
            name='pub_date',
            field=models.DateField(auto_now=True),
        ),
    ]
