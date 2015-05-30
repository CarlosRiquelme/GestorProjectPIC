# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0002_auto_20150529_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='estado',
            field=models.CharField(default=b'CREADO', max_length=30, choices=[(b'CREADO', b'CREADO'), (b'TODO', b'TODO'), (b'DOING', b'DOING'), (b'DONE', b'DONE'), (b'REASIGNAR_SPRINT', b'REASIGNAR_SPRINT'), (b'REASIGNAR_ACTIVIDAD', b'REASIGNAR_ACTIVIDAD'), (b'FINALIZADO', b'FINALIZADO')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='porcentaje',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
