# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0004_auto_20150618_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='suma_tiempo',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='estado',
            field=models.CharField(default=b'CREADO', max_length=30, choices=[(b'CREADO', b'CREADO'), (b'TODO', b'TODO'), (b'DOING', b'DOING'), (b'DONE', b'DONE'), (b'REASIGNAR_SPRINT', b'REASIGNAR_SPRINT'), (b'REASIGNAR_ACTIVIDAD', b'REASIGNAR_ACTIVIDAD'), (b'FINALIZADO', b'FINALIZADO'), (b'CANCELADO', b'CANCELADO'), (b'REVISAR', b'REVISAR'), (b'REVISAR_E', b'REVISAR_E')]),
            preserve_default=True,
        ),
    ]
