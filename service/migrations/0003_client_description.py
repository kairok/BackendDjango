# Generated by Django 2.0.6 on 2019-09-17 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20190916_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
