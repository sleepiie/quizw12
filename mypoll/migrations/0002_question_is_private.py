# Generated by Django 5.1.3 on 2025-03-13 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypoll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
