# Generated by Django 3.2.4 on 2021-08-21 21:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adventure', '0003_auto_20210821_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='videoPathPreset',
        ),
    ]
