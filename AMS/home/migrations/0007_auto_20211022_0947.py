# Generated by Django 3.2.8 on 2021-10-22 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20211022_0752'),
    ]

    operations = [
        migrations.AddField(
            model_name='professor',
            name='profprofilepic',
            field=models.FileField(blank=True, null=True, upload_to='pictures/'),
        ),
        migrations.AddField(
            model_name='student',
            name='studprofilepic',
            field=models.FileField(blank=True, null=True, upload_to='pictures/'),
        ),
    ]
