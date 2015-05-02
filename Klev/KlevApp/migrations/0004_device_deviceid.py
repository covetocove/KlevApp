# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KlevApp', '0003_device_nodeid'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='deviceid',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
