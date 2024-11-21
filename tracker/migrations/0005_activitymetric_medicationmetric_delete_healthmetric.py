# Generated by Django 5.1.3 on 2024-11-20 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_alter_healthmetric_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('calories', models.IntegerField(blank=True, null=True)),
                ('activity_minutes', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MedicationMetric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('medication_name', models.CharField(max_length=100)),
                ('medication_dose', models.CharField(max_length=100)),
                ('vitamin_name', models.CharField(blank=True, max_length=100, null=True)),
                ('vitamin_dose', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='HealthMetric',
        ),
    ]
