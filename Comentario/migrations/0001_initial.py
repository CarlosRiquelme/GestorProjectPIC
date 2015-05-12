# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0006_userstory_tiempo_estimado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=120, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now=True)),
                ('adjunto', models.FileField(null=True, upload_to=b'documents')),
                ('porcentaje', models.IntegerField(null=True)),
                ('hora_trabajada', models.IntegerField(null=True)),
                ('userstory', models.ForeignKey(to='UserStory.UserStory', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
