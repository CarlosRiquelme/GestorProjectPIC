# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0005_auto_20150501_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='tiempo_estimado',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
