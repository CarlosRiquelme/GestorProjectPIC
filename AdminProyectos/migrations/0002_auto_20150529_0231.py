# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminProyectos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='descripcion',
            field=models.CharField(max_length=120, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(default=b'EN-ESPERA', max_length=30, choices=[(b'EN-ESPERA', b'EN-ESPERA'), (b'EN-DESARROLLO', b'EN-DESARROLLO'), (b'FINALIZADO', b'FINALIZADO'), (b'CANCELADO', b'CANCELADO')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fechaFin',
            field=models.DateField(null=True, verbose_name=b'Fecha de Fin'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fechaInicio',
            field=models.DateField(null=True, verbose_name=b'Fecha de Inicio'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='nombre',
            field=models.CharField(max_length=30, unique=True, null=True),
            preserve_default=True,
        ),
    ]
