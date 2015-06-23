# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0006_auto_20150619_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='estado',
            field=models.CharField(default=b'CREADO', max_length=30, choices=[(b'CREADO', b'CREADO'), (b'TODO', b'TODO'), (b'DOING', b'DOING'), (b'DONE', b'DONE'), (b'REASIGNAR_SPRINT', b'REASIGNAR_SPRINT'), (b'REASIGNAR_ACTIVIDAD', b'REASIGNAR_ACTIVIDAD'), (b'FINALIZADO', b'FINALIZADO'), (b'CANCELADO', b'CANCELADO'), (b'REVISAR', b'REVISAR'), (b'REVISAR_E', b'REVISAR_E'), (b'REVISAR_FIN_AC', b'REVISAR_FIN_AC')]),
            preserve_default=True,
        ),
    ]
