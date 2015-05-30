# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='cantidad_userstory',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sprint',
            name='dia_trancurrido',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sprint',
            name='dias_duracion',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sprint',
            name='porcentaje_actual',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sprint',
            name='porcentaje_hecho_actual',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
