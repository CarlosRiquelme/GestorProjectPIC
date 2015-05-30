# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminProyectos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimacion_Proyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaInicio', models.DateField(null=True)),
                ('fechaFin', models.DateField(null=True)),
                ('proyecto', models.ForeignKey(to='AdminProyectos.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estimacion_Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaInicio', models.DateField(null=True)),
                ('fechaFin', models.DateField(null=True)),
                ('duracion', models.IntegerField()),
                ('proyecto_estimacion', models.ForeignKey(to='Sprint.Estimacion_Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fechaInicio', models.DateField(null=True)),
                ('tiempo_acumulado', models.IntegerField(default=0, null=True)),
                ('estado', models.CharField(default=b'ABIERTO', max_length=30, choices=[(b'EN-ESPERA', b'EN-ESPERA'), (b'ABIERTO', b'ABIERTO'), (b'CERRADO', b'CERRADO')])),
                ('secuencia', models.IntegerField()),
                ('proyecto', models.ForeignKey(to='AdminProyectos.Proyecto', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='estimacion_sprint',
            name='sprint',
            field=models.ForeignKey(to='Sprint.Sprint'),
            preserve_default=True,
        ),
    ]
