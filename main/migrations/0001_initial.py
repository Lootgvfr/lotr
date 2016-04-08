# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=500)),
                ('ip_address', models.CharField(max_length=30)),
                ('add_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100, unique=True)),
                ('add_date', models.DateField()),
                ('order', models.IntegerField(unique=True)),
                ('pic', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('text', models.CharField(max_length=1000)),
                ('order', models.IntegerField(unique=True)),
                ('page', models.ForeignKey(to='main.Page')),
            ],
        ),
    ]
