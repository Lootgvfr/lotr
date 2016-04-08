# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20160112_1657'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.CharField(max_length=100)),
                ('votes_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('text', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=50)),
                ('answer_count', models.IntegerField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='page',
            options={},
        ),
        migrations.AlterField(
            model_name='page',
            name='tags',
            field=models.ManyToManyField(to='main.Tag'),
        ),
        migrations.AddField(
            model_name='profile',
            name='votes',
            field=models.ManyToManyField(to='main.Question'),
        ),
    ]
