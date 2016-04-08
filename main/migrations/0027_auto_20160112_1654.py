# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_tagpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagpage',
            name='page',
        ),
        migrations.RemoveField(
            model_name='tagpage',
            name='tag',
        ),
        migrations.AddField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(to='main.Tag'),
        ),
        migrations.DeleteModel(
            name='TagPage',
        ),
    ]
