# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=60)),
                ('descripcion', models.CharField(max_length=120)),
                ('fechaCreacion', models.DateTimeField(verbose_name=b'Fecha de Creacion')),
                ('fechaInicio', models.DateTimeField(verbose_name=b'Fecha de Inicio')),
                ('fechaFin', models.DateTimeField(verbose_name=b'Fecha de Fin')),
                ('duracionEstimada', models.CharField(max_length=20)),
                ('estado', models.CharField(max_length=40)),
                ('usuarios', models.ManyToManyField(related_name='proyectos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
