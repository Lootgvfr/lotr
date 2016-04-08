# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20151109_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='answer',
            field=models.CharField(null=True, max_length=500),
        ),
        migrations.AddField(
            model_name='page',
            name='added_by',
            field=models.CharField(null=True, max_length=30),
        ),
    ]
