# Generated by Django 2.0.6 on 2019-09-23 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_client_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='master',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]