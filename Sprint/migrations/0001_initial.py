# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Flujo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fechaInicio', models.DateField(verbose_name=b'Fecha de Inicio')),
                ('fechaFin', models.DateField(verbose_name=b'Fecha de Fin')),
                ('tiempo_acumulado', models.IntegerField(default=0, null=True)),
                ('estado', models.CharField(default=b'ABIERTO', max_length=30, choices=[(b'ABIERTO', b'ABIERTO'), (b'CERRADO', b'CERRADO')])),
                ('flujo', models.ForeignKey(to='Flujo.Flujo', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
