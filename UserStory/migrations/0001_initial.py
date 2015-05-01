# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Actividades', '0001_initial'),
        ('Sprint', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('descripcion', models.CharField(unique=True, max_length=150)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fechaInicio', models.DateField(verbose_name=b'Fecha de Inicio')),
                ('fechaFin', models.DateField(verbose_name=b'Fecha de Fin')),
                ('estado', models.CharField(default=b'TODO', max_length=30, choices=[(b'TODO', b'TODO'), (b'DOING', b'DOING'), (b'DONE', b'DONE')])),
                ('priodidad', models.CharField(default=b'TODO', max_length=30, choices=[(b'BAJA', b'BAJA'), (b'MEDIA', b'MEDIA'), (b'ALTA', b'ALTA')])),
                ('tiempo_trabajado', models.IntegerField(null=True)),
                ('porcentaje', models.IntegerField(null=True)),
                ('actividad', models.ForeignKey(to='Actividades.Actividad', null=True)),
                ('sprint', models.ForeignKey(to='Sprint.Sprint', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
