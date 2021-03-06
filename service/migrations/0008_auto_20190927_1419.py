# Generated by Django 2.0.6 on 2019-09-27 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_auto_20190927_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='firma',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.Firma'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='master',
            name='firma',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.Firma'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='problem',
            name='firma',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.Firma'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='firma',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.Firma'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spec',
            name='firma',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='service.Firma'),
            preserve_default=False,
        ),
    ]
