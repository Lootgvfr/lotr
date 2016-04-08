# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_tag'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagPage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('page', models.ForeignKey(to='main.Page')),
                ('tag', models.ForeignKey(to='main.Tag')),
            ],
        ),
    ]
