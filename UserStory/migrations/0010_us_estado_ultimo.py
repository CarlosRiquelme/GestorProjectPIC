# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0009_auto_20150701_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='US_Estado_ultimo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado', models.CharField(max_length=30)),
                ('us', models.ForeignKey(to='UserStory.UserStory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
