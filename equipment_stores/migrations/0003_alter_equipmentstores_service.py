# Generated by Django 4.0.4 on 2022-06-21 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment_stores', '0002_alter_equipmentstores_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentstores',
            name='service',
            field=models.CharField(choices=[(1, 'Sale'), (2, 'Rent'), (3, 'Sale|Rent'), (4, 'Other')], max_length=11, null=True),
        ),
    ]