# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0003_sprint_fechafin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='estado',
            field=models.CharField(default=b'EN-ESPERA', max_length=30, choices=[(b'EN-ESPERA', b'EN-ESPERA'), (b'ABIERTO', b'ABIERTO'), (b'CERRADO', b'CERRADO')]),
            preserve_default=True,
        ),
    ]
