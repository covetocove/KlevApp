# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KlevApp', '0004_device_deviceid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='deviceid',
        ),
    ]
