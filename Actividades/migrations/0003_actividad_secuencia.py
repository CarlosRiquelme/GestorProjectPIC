# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Actividades', '0002_remove_actividad_secuencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='secuencia',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
