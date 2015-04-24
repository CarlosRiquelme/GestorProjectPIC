# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('PIC', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flujo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=60)),
                ('tiempo_estimado', models.IntegerField()),
                ('estado', models.CharField(max_length=40)),
                ('proyecto', models.ForeignKey(to='PIC.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Usuario_Rol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rol', models.ForeignKey(to='auth.Group')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='proyecto',
            name='usuarios',
        ),
        migrations.AddField(
            model_name='proyecto',
            name='rol_usuario',
            field=models.ManyToManyField(related_name='proyectos', to='PIC.Usuario_Rol'),
            preserve_default=True,
        ),
    ]
