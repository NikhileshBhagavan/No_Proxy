# Generated by Django 3.2.8 on 2021-10-29 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_absentdates_attendanceid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absentdates',
            name='dates_of_absent',
            field=models.DateField(blank=True, null=True),
        ),
    ]
