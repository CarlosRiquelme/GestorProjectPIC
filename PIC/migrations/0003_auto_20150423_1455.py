# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PIC', '0002_auto_20150423_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(default=b'NO-INICIADO', max_length=40, choices=[(b'NO-INICIADO', b'NO-INICIADO'), (b'INICIADO', b'INICIADO')]),
            preserve_default=True,
        ),
    ]
