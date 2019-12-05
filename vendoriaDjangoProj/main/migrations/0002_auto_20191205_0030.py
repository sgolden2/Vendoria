# Generated by Django 2.2.7 on 2019-12-05 06:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Region'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchase',
            name='DOT',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 5, 0, 30, 33, 227730)),
        ),
    ]
