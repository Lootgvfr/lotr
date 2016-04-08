# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_user_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='paragraph',
            name='order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
