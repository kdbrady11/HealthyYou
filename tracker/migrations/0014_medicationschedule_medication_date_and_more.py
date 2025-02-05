# Generated by Django 5.1.3 on 2025-01-22 22:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0013_alter_medicationschedule_dosage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicationschedule',
            name='medication_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='medicationschedule',
            name='dosage',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='medicationschedule',
            name='medication_name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='medicationschedule',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='medicationschedule',
            name='time_of_day',
            field=models.TimeField(),
        ),
    ]
