# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.CharField(max_length=128, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('location', models.CharField(max_length=512, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.CharField(max_length=128, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=128, blank=True)),
                ('website', models.CharField(max_length=256, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='vendors',
            field=models.ManyToManyField(related_name='events', to='offthegrid.Vendor'),
        ),
    ]
