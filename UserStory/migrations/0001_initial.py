# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0001_initial'),
        ('AdminProyectos', '__first__'),
        ('Actividades', '0002_actividad_flujo'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('descripcion', models.CharField(max_length=150)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fechaInicio', models.DateField(verbose_name=b'Fecha de Inicio')),
                ('fechaFin', models.DateField(verbose_name=b'Fecha de Fin')),
                ('estado', models.CharField(default=b'CREADO', max_length=30, choices=[(b'CREADO', b'CREADO'), (b'TODO', b'TODO'), (b'DOING', b'DOING'), (b'DONE', b'DONE')])),
                ('prioridad', models.CharField(default=b'BAJA', max_length=30, null=True, choices=[(b'BAJA', b'BAJA'), (b'MEDIA', b'MEDIA'), (b'ALTA', b'ALTA')])),
                ('tiempo_trabajado', models.IntegerField(null=True)),
                ('porcentaje', models.IntegerField(null=True)),
                ('actividad', models.ForeignKey(to='Actividades.Actividad', null=True)),
                ('proyecto', models.ForeignKey(to='AdminProyectos.Proyecto', null=True)),
                ('sprint', models.ForeignKey(to='Sprint.Sprint', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
