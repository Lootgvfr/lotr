# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_paragraph_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paragraph',
            name='order',
        ),
    ]
