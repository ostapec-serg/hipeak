# Generated by Django 4.0.4 on 2022-06-30 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration_authorisation', '0003_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
    ]
