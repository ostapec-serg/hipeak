# Generated by Django 4.0.4 on 2022-06-21 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment_stores', '0004_alter_equipmentstores_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipmentstores',
            name='service',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Sale'), (2, 'Rent'), (3, 'Sale|Rent'), (4, 'Other')], null=True),
        ),
    ]