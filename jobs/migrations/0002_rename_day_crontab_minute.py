# Generated by Django 3.2.8 on 2021-10-28 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crontab',
            old_name='day',
            new_name='minute',
        ),
    ]
