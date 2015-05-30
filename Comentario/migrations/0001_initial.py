# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=120, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('porcentaje', models.IntegerField(null=True)),
                ('hora_trabajada', models.IntegerField(null=True)),
                ('adjunto', models.NullBooleanField()),
                ('userstory', models.ForeignKey(to='UserStory.UserStory', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'documents/%Y/%m/%d')),
                ('comentario', models.ForeignKey(to='Comentario.Comentario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
