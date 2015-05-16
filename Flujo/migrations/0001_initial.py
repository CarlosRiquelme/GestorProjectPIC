# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminProyectos', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flujo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('cantidad_de_actividades', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(default=b'NO-CREADO', max_length=30, choices=[(b'NO-CREADO', b'NO-CREADO'), (b'CREADO', b'CREADO')])),
                ('proyecto', models.ForeignKey(to='AdminProyectos.Proyecto', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
