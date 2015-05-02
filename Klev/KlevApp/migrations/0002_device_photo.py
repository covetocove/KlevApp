# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('KlevApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='photo',
            field=models.ImageField(default=None, null=True, upload_to=b'deviceImages', blank=True),
            preserve_default=True,
        ),
    ]
