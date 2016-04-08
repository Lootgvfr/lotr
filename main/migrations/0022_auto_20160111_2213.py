# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0021_auto_20160111_2209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('phone', models.CharField(null=True, max_length=20)),
                ('phone_show', models.CharField(null=True, max_length=3)),
                ('about', models.CharField(null=True, max_length=300)),
                ('about_show', models.CharField(null=True, max_length=3)),
                ('city', models.CharField(null=True, max_length=50)),
                ('city_show', models.CharField(null=True, max_length=3)),
                ('groupname', models.CharField(max_length=20)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='user_info',
            name='user',
        ),
        migrations.DeleteModel(
            name='User_info',
        ),
    ]
