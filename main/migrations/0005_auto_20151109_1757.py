# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20151108_1628'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={'permissions': (('view_hidden', 'Can view hidden articles'), ('view_user_only', 'Can view user-only articles'), ('view_admin_panel', 'Can view administration panel'))},
        ),
    ]
