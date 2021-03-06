# Generated by Django 4.0.4 on 2022-06-21 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration_authorisation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Закладка. Організації',
                'verbose_name_plural': 'Закладки. Організації',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Категорія',
                'verbose_name_plural': 'Категорії',
            },
        ),
        migrations.CreateModel(
            name='Organisations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('url', models.URLField(blank=True, null=True)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Contact phone number', max_length=128, region=None)),
                ('email', models.EmailField(error_messages={'unique': 'A organisation with that email already exists.'}, max_length=254, unique=True)),
                ('img', models.ImageField(blank='true', null=True, upload_to='organisations/', verbose_name='organisation_img')),
                ('category', models.ManyToManyField(to='tours.category')),
            ],
            options={
                'verbose_name': 'Організація',
                'verbose_name_plural': 'Організації',
            },
        ),
        migrations.CreateModel(
            name='TourBookmarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Закладка. Тури',
                'verbose_name_plural': 'Закладки. Тури',
            },
        ),
        migrations.CreateModel(
            name='TourComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=300)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('moderate_status', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Коментар туру',
                'verbose_name_plural': 'Коментарі турів',
            },
        ),
        migrations.CreateModel(
            name='TourRatings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 'Ok'), (2, 'Fine'), (3, 'Good'), (4, 'Nice'), (5, 'Amazing')], null=True)),
            ],
            options={
                'verbose_name': 'Рейтинг туру',
                'verbose_name_plural': 'Рейтинг турів',
            },
        ),
        migrations.CreateModel(
            name='Tours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('food', models.CharField(choices=[(1, 'RO(room only)'), (2, 'HB(half board)'), (3, 'FB(full board)'), (4, 'AI(all inclusive)')], max_length=25)),
                ('transfer', models.BooleanField(default=False)),
                ('flying', models.BooleanField(default=False)),
                ('residence', models.CharField(choices=[(1, 'Camp'), (2, 'Camp|Hotel'), (3, 'Hotel')], max_length=10)),
                ('price', models.PositiveIntegerField()),
                ('start_date', models.DateField()),
                ('finish_date', models.DateField()),
                ('currency', models.CharField(choices=[(1, 'UAH'), (2, 'USD'), (3, 'EUR')], max_length=25, null=True)),
                ('img', models.ImageField(blank='true', null=True, upload_to='tours/', verbose_name='tours_img')),
                ('is_active', models.BooleanField(default=False)),
                ('comment', models.ManyToManyField(related_name='tour_comment', through='tours.TourComments', to=settings.AUTH_USER_MODEL)),
                ('in_bookmarks', models.ManyToManyField(related_name='tour_bookmarks', through='tours.TourBookmarks', to=settings.AUTH_USER_MODEL)),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tours.organisations')),
                ('rating', models.ManyToManyField(related_name='tour_rating', through='tours.TourRatings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Тур',
                'verbose_name_plural': 'Тури',
            },
        ),
        migrations.AddField(
            model_name='tourratings',
            name='rate_article',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.tours'),
        ),
        migrations.AddField(
            model_name='tourratings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.fields.NOT_PROVIDED, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tourcomments',
            name='article_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.tours'),
        ),
        migrations.AddField(
            model_name='tourcomments',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.fields.NOT_PROVIDED, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tourbookmarks',
            name='tour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.tours'),
        ),
        migrations.AddField(
            model_name='tourbookmarks',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, 'Ok'), (2, 'Fine'), (3, 'Good'), (4, 'Nice'), (5, 'Amazing')], null=True)),
                ('rate_article', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.organisations')),
                ('user', models.ForeignKey(on_delete=django.db.models.fields.NOT_PROVIDED, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Рейтинг організації',
                'verbose_name_plural': 'Рейтинг організацій',
            },
        ),
        migrations.CreateModel(
            name='OrganisationsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.CharField(max_length=150)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('moderate_status', models.BooleanField(default=False)),
                ('article_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.organisations')),
                ('author', models.ForeignKey(default='user', on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Коментар організаціЇ',
                'verbose_name_plural': 'Коментарі організацій',
            },
        ),
        migrations.AddField(
            model_name='organisations',
            name='comment',
            field=models.ManyToManyField(related_name='organisation_comment', through='tours.OrganisationsComment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organisations',
            name='in_bookmarks',
            field=models.ManyToManyField(related_name='user_bookmarks', through='tours.Bookmarks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='organisations',
            name='rating',
            field=models.ManyToManyField(related_name='organisation_rating', through='tours.Ratings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookmarks',
            name='organisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tours.organisations'),
        ),
        migrations.AddField(
            model_name='bookmarks',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
