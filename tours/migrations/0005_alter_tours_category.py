# Generated by Django 4.0.4 on 2022-06-22 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0004_tours_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tours',
            name='category',
            field=models.ManyToManyField(help_text="Щоб обрати декілька категорій, зажміть 'alt' або 'command'", related_name='tour_category', to='tours.category'),
        ),
    ]
