# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminProyectos', '0001_initial'),
        ('Sprint', '0005_sprint_suma_tiempo_usestory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto_En_Proceso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(null=True)),
                ('horas_acumulada_sprint', models.IntegerField(null=True)),
                ('proyecto', models.ForeignKey(to='AdminProyectos.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sprint_En_Proceso',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(null=True)),
                ('horas_acumulada', models.IntegerField(null=True)),
                ('sprint', models.ForeignKey(to='Sprint.Sprint')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
