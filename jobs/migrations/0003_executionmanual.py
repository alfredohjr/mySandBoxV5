# Generated by Django 3.2.8 on 2021-11-03 19:44

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_rename_day_crontab_minute'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExecutionManual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=0)),
                ('run', models.BooleanField(default=True)),
                ('startAt', models.DateTimeField(default=django.utils.timezone.now)),
                ('finishedAt', models.DateTimeField()),
                ('script', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.scripts')),
            ],
        ),
    ]
