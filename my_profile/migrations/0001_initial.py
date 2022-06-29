# Generated by Django 4.0.4 on 2022-06-21 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(auto_created=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='profile_img/', verbose_name='Фото профілю')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Contact phone number', max_length=128, region=None, verbose_name='Номер телефону')),
                ('bio', models.CharField(blank=True, max_length=160, null=True, verbose_name='Біографія')),
                ('birthday', models.DateField(blank=True, help_text='В форматі дд.мм.рр.!', null=True, verbose_name='Дата народження')),
                ('email_subscribe', models.BooleanField(default=True, verbose_name='Підписка на почтову розсилку')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Користувач')),
            ],
            options={
                'verbose_name': 'Прфіль',
                'verbose_name_plural': 'Профілі',
            },
        ),
    ]
