# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20151106_0002'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='access',
            field=models.CharField(default='anon', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='page',
            name='status',
            field=models.CharField(default='published', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paragraph',
            name='title',
            field=models.CharField(default='title', max_length=100),
            preserve_default=False,
        ),
    ]
