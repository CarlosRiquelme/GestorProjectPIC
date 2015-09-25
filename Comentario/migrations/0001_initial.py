# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bytes', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('mimetype', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=120, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('porcentaje_actividad', models.IntegerField(null=True)),
                ('hora_trabajada', models.IntegerField(null=True)),
                ('porcentaje_userstory', models.FloatField(null=True)),
                ('adjunto', models.NullBooleanField()),
                ('userstory', models.ForeignKey(to='UserStory.UserStory', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(null=True, upload_to=b'Comentario.Archivo/bytes/filename/mimetype', blank=True)),
                ('comentario', models.ForeignKey(to='Comentario.Comentario')),
            ],
        ),
    ]
