# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_paragraph_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_info',
            name='name',
        ),
        migrations.AddField(
            model_name='user_info',
            name='about',
            field=models.CharField(null=True, max_length=300),
        ),
        migrations.AddField(
            model_name='user_info',
            name='about_show',
            field=models.CharField(null=True, max_length=3),
        ),
        migrations.AddField(
            model_name='user_info',
            name='city',
            field=models.CharField(null=True, max_length=50),
        ),
        migrations.AddField(
            model_name='user_info',
            name='city_show',
            field=models.CharField(null=True, max_length=3),
        ),
        migrations.AddField(
            model_name='user_info',
            name='phone_show',
            field=models.CharField(null=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='user_info',
            name='groupname',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='user_info',
            name='phone',
            field=models.CharField(null=True, max_length=20),
        ),
    ]
