# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20151113_0519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paragraph',
            name='order',
            field=models.IntegerField(default='1'),
        ),
    ]
