# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20151113_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paragraph',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
