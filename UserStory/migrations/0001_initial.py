# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('Actividades', '0001_initial'),
        ('Sprint', '0001_initial'),
        ('AdminProyectos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('descripcion', models.CharField(max_length=150)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(default=b'CREADO', max_length=30, choices=[(b'CREADO', b'CREADO'), (b'TODO', b'TODO'), (b'DOING', b'DOING'), (b'DONE', b'DONE')])),
                ('prioridad', models.CharField(max_length=30)),
                ('tiempo_trabajado', models.IntegerField(null=True)),
                ('porcentaje', models.IntegerField(null=True)),
                ('tiempo_estimado', models.IntegerField(null=True)),
                ('actividad', models.ForeignKey(to='Actividades.Actividad', null=True)),
                ('proyecto', models.ForeignKey(to='AdminProyectos.Proyecto', null=True)),
                ('sprint', models.ForeignKey(to='Sprint.Sprint', null=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
