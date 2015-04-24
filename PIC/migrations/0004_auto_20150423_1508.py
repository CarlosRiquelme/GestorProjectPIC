# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PIC', '0003_auto_20150423_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flujo',
            name='estado',
            field=models.CharField(default=b'EN-ESPERA', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(default=b'EN-ESPERA', max_length=40, choices=[(b'EN-ESPERA', b'EN-ESPERA'), (b'EN-DESARROLLO', b'EN-DESARROLLO'), (b'FINALIZADO', b'FINALIZADO')]),
            preserve_default=True,
        ),
    ]
