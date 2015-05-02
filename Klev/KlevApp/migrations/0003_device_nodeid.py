# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KlevApp', '0002_device_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='nodeid',
            field=models.IntegerField(default=-1),
            preserve_default=True,
        ),
    ]
