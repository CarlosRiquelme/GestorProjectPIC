# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Flujo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flujo',
            name='estado',
            field=models.CharField(default=b'NO-CREADO', max_length=30, choices=[(b'NO-CREADO', b'NO-CREADO'), (b'CREADO', b'CREADO')]),
            preserve_default=True,
        ),
    ]
