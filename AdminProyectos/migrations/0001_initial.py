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
                ('nombre', models.CharField(max_length=30, unique=True, null=True)),
                ('descripcion', models.CharField(max_length=120, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('fechaInicio', models.DateField(null=True, verbose_name=b'Fecha de Inicio')),
                ('fechaFin', models.DateField(null=True, verbose_name=b'Fecha de Fin')),
                ('estado', models.CharField(default=b'EN-ESPERA', max_length=30, choices=[(b'EN-ESPERA', b'EN-ESPERA'), (b'EN-DESARROLLO', b'EN-DESARROLLO'), (b'FINALIZADO', b'FINALIZADO'), (b'CANCELADO', b'CANCELADO'), (b'REVISAR', b'REVISAR')])),
                ('scrumMaster', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]