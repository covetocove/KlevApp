# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('deviceName', models.CharField(max_length=42)),
                ('make', models.CharField(max_length=42)),
                ('modelNum', models.CharField(max_length=42)),
                ('location', models.CharField(max_length=80)),
                ('deviceState', models.CharField(max_length=20)),
                ('trained', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=80)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
