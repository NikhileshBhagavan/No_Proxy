# Generated by Django 3.2.8 on 2021-10-27 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_attendance_limits'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='attended_status',
            field=models.BooleanField(default=False),
        ),
    ]
