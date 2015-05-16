# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='prioridad',
            field=models.CharField(max_length=30),
            preserve_default=True,
        ),
    ]
