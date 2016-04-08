# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_auto_20160111_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_show',
            field=models.CharField(null=True, max_length=3),
        ),
    ]
