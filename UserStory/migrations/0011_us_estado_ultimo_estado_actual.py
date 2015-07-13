# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0010_us_estado_ultimo'),
    ]

    operations = [
        migrations.AddField(
            model_name='us_estado_ultimo',
            name='estado_actual',
            field=models.CharField(default=1, max_length=30),
            preserve_default=False,
        ),
    ]
