# Generated by Django 5.2 on 2025-05-20 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_appointment_appointment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
