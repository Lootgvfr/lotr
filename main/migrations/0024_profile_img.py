# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_profile_email_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='img',
            field=models.FileField(null=True, upload_to=main.models.generate_filename),
        ),
    ]
