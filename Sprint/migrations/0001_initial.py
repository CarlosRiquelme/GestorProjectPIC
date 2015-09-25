# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminProyectos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dias_de_un_Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dia', models.IntegerField(null=True)),
                ('fecha', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estimacion_Proyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fechaInicio', models.DateField(null=True)),
                ('fechaFin', models.DateField(null=True)),
                ('proyecto', models.ForeignKey(to='AdminProyectos.Proyecto')),
            ],
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
        ),
        migrations.CreateModel(
            name='Proyecto_En_Proceso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(null=True)),
                ('horas_acumulada_sprint', models.IntegerField(null=True)),
                ('proyecto', models.ForeignKey(to='AdminProyectos.Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fechaInicio', models.DateField(null=True)),
                ('fechaFin', models.DateField(null=True)),
                ('tiempo_acumulado', models.IntegerField(default=0, null=True)),
                ('suma_tiempo_usestory', models.IntegerField(default=0, null=True)),
                ('estado', models.CharField(default=b'EN-ESPERA', max_length=30, choices=[(b'EN-ESPERA', b'EN-ESPERA'), (b'ABIERTO', b'ABIERTO'), (b'CERRADO', b'CERRADO')])),
                ('secuencia', models.IntegerField()),
                ('dias_duracion', models.IntegerField(null=True)),
                ('cantidad_userstory', models.IntegerField(null=True)),
                ('porcentaje_actual', models.FloatField(null=True)),
                ('porcentaje_hecho_actual', models.FloatField(null=True)),
                ('dia_trancurrido', models.IntegerField(null=True)),
                ('proyecto', models.ForeignKey(to='AdminProyectos.Proyecto', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sprint_En_Proceso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(null=True)),
                ('horas_acumulada', models.IntegerField(null=True)),
                ('sprint', models.ForeignKey(to='Sprint.Sprint')),
            ],
        ),
        migrations.AddField(
            model_name='estimacion_sprint',
            name='sprint',
            field=models.ForeignKey(to='Sprint.Sprint'),
        ),
        migrations.AddField(
            model_name='dias_de_un_sprint',
            name='sprint',
            field=models.ForeignKey(to='Sprint.Sprint'),
        ),
    ]
