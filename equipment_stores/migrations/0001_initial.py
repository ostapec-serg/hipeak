# Generated by Django 4.0.4 on 2022-06-21 09:02

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EquipmentStores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва')),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(verbose_name='Опис')),
                ('url', models.URLField(null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Contact phone number', max_length=128, region=None, verbose_name='Номер телефону')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('store_address', models.CharField(max_length=150, verbose_name='Адресв')),
                ('is_active', models.BooleanField(default=False)),
                ('location', models.CharField(blank=True, max_length=500)),
                ('service', models.CharField(choices=[(1, 'Sale'), (2, 'Rent'), (3, 'Sale|Rent'), (4, 'Other')], max_length=11)),
                ('img', models.ImageField(blank='true', null=True, upload_to='stores_images/', verbose_name='stores_images/')),
            ],
            options={
                'verbose_name': 'Магазин',
                'verbose_name_plural': 'Магазини',
            },
        ),
    ]
