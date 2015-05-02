# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KlevApp', '0005_remove_device_deviceid'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='address',
            field=models.CharField(default=15, max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='device',
            name='city',
            field=models.CharField(default=23, max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='device',
            name='state',
            field=models.CharField(default=13, max_length=80),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='device',
            name='zipCode',
            field=models.CharField(default=34, max_length=10),
            preserve_default=False,
        ),
    ]
