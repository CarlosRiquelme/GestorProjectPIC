# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Flujo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fechaInicio', models.DateField(verbose_name=b'Fecha de Inicio')),
                ('fechaFin', models.DateField(verbose_name=b'Fecha de Fin')),
                ('estado', models.CharField(default=b'PROGRAMADO', max_length=30, choices=[(b'PROGRAMADO', b'PROGRAMADO'), (b'INICIADO', b'INICIADO'), (b'FINALIZADO', b'FINALIZADO')])),
                ('secuencia', models.IntegerField(null=True)),
                ('flujo', models.ForeignKey(to='Flujo.Flujo', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
