# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0004_auto_20150530_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='suma_tiempo_usestory',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
