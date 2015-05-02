# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0002_auto_20150501_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='descripcion',
            field=models.CharField(max_length=150),
            preserve_default=True,
        ),
    ]
