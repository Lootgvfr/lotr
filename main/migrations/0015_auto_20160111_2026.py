# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20160111_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paragraph',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
