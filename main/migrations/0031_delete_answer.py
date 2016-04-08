# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20160112_2015'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Answer',
        ),
    ]
