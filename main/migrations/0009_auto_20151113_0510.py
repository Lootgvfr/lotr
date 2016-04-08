# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_auto_20151111_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='pic',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='order',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='paragraph',
            name='text',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
