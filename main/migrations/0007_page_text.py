# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20151109_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='text',
            field=models.CharField(null=True, max_length=1000),
        ),
    ]
