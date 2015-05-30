# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comentario',
            old_name='porcentaje',
            new_name='porcentaje_actividad',
        ),
        migrations.AddField(
            model_name='comentario',
            name='porcentaje_userstory',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
