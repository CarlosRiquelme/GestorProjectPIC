# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0006_userstory_tiempo_estimado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='prioridad',
            field=models.CharField(default=b'BAJA', max_length=30, choices=[(b'BAJA', b'BAJA'), (b'MEDIA', b'MEDIA'), (b'ALTA', b'ALTA')]),
            preserve_default=True,
        ),
    ]
