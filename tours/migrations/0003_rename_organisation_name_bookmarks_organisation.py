# Generated by Django 4.0.3 on 2022-05-10 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0002_organisations_in_bookmarks_organisations_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookmarks',
            old_name='organisation_name',
            new_name='organisation',
        ),
    ]