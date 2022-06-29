# Generated by Django 4.0.4 on 2022-06-23 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0006_alter_tours_food_alter_tours_residence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tours',
            name='currency',
            field=models.CharField(choices=[(1, 'UAH')], max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='tours',
            name='food',
            field=models.CharField(choices=[('room only', 'RO(room only)'), ('half board', 'HB(half board)'), ('full board', 'FB(full board)'), ('all inclusive', 'AI(all inclusive)')], max_length=13, null=True),
        ),
        migrations.AlterField(
            model_name='tours',
            name='residence',
            field=models.CharField(choices=[('camp', 'Camp'), ('camp|hotel', 'Camp|Hotel'), ('hotel', 'Hotel')], max_length=17, null=True),
        ),
    ]
