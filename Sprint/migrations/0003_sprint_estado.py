# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0002_sprint_flujo'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='estado',
            field=models.CharField(default=b'ABIERTO', max_length=30, choices=[(b'ABIERTO', b'ABIERTO'), (b'CERRADO', b'CERRADO')]),
            preserve_default=True,
        ),
    ]
