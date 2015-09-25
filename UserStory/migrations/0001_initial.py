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
            name='US_Estado_ultimo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('estado', models.CharField(max_length=30)),
                ('estado_actual', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=30)),
                ('descripcion', models.CharField(max_length=150)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('estado', models.CharField(default=b'CREADO', max_length=30, choices=[(b'CREADO', b'CREADO'), (b'TODO', b'TODO'), (b'DOING', b'DOING'), (b'DONE', b'DONE'), (b'REASIGNAR_SPRINT', b'REASIGNAR_SPRINT'), (b'REASIGNAR_ACTIVIDAD', b'REASIGNAR_ACTIVIDAD'), (b'FINALIZADO', b'FINALIZADO'), (b'CANCELADO', b'CANCELADO'), (b'REVISAR_TIEMPO', b'REVISAR_TIEMPO'), (b'REVISAR', b'REVISAR'), (b'REVISAR_E', b'REVISAR_E'), (b'REVISAR_FIN_AC', b'REVISAR_FIN_AC'), (b'REVISAR_FIN', b'REVISAR_FIN')])),
                ('prioridad', models.CharField(max_length=30)),
                ('tiempo_trabajado', models.IntegerField(null=True)),
                ('suma_trabajadas', models.IntegerField(default=0, null=True)),
                ('porcentaje', models.FloatField(null=True)),
                ('tiempo_estimado', models.IntegerField(default=0, null=True)),
                ('nro_sprint', models.IntegerField(null=True)),
                ('nro_actividad', models.IntegerField(null=True)),
                ('porcentaje_actividad', models.FloatField(null=True)),
                ('actividad', models.ForeignKey(to='Actividades.Actividad', null=True)),
                ('proyecto', models.ForeignKey(to='AdminProyectos.Proyecto', null=True)),
                ('sprint', models.ForeignKey(to='Sprint.Sprint', null=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='us_estado_ultimo',
            name='us',
            field=models.ForeignKey(to='UserStory.UserStory'),
        ),
    ]
