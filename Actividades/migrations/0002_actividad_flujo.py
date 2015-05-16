# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Actividades', '0001_initial'),
        ('Flujo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='flujo',
            field=models.ForeignKey(to='Flujo.Flujo', null=True),
            preserve_default=True,
        ),
    ]
