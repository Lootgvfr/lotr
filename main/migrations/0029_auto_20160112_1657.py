# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_auto_20160112_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(null=True, to='main.Tag'),
        ),
    ]
