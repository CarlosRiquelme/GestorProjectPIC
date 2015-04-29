# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=20)),
                ('contenido', models.TextField(max_length=200)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('hora_trabajada', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Flujo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=60)),
                ('tiempo_estimado', models.IntegerField()),
                ('estado', models.CharField(default=b'EN-ESPERA', max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
                ('estado', models.CharField(default=b'EN-ESPERA', max_length=40, choices=[(b'EN-ESPERA', b'EN-ESPERA'), (b'EN-DESARROLLO', b'EN-DESARROLLO'), (b'FINALIZADO', b'FINALIZADO')])),
                ('scrumMaster', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=60)),
                ('fechaCreacion', models.DateTimeField(verbose_name=b'Fecha de Creacion')),
                ('fechaInicio', models.DateTimeField(verbose_name=b'Fecha de Inicio')),
                ('fechaFinEstimado', models.DateTimeField(verbose_name=b'Fecha de Fin Estimado')),
                ('tiempoEstimado', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=40)),
                ('descripcion', models.TextField(max_length=120)),
                ('tiempo_estimado', models.IntegerField()),
                ('tiempo_trabajado', models.IntegerField(default=0)),
                ('fecha_inicio', models.DateTimeField(verbose_name=b'Fecha de Inicio')),
                ('fecha_fin', models.DateTimeField(verbose_name=b'Fecha Fin')),
                ('activo', models.BooleanField(default=False)),
                ('flujo', models.ForeignKey(to='PIC.Flujo')),
                ('proyecto', models.ForeignKey(to='PIC.Proyecto')),
                ('sprint', models.ForeignKey(to='PIC.Sprint')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Story',
                'verbose_name_plural': 'User Story',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario_rol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('usario_Rol', models.CharField(max_length=40)),
                ('rol', models.ForeignKey(to='auth.Group')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Asignar Rol a User',
                'verbose_name_plural': 'Asignar Rol a User',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='usuario_rol',
            field=models.ManyToManyField(related_name='proyectos', to='PIC.Usuario_rol'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flujo',
            name='proyecto',
            field=models.ForeignKey(to='PIC.Proyecto', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comentario',
            name='user_story',
            field=models.ForeignKey(to='PIC.User_Story'),
            preserve_default=True,
        ),
    ]
