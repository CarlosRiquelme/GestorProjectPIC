# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PIC', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='user_story',
        ),
        migrations.DeleteModel(
            name='Comentario',
        ),
        migrations.RemoveField(
            model_name='flujo',
            name='proyecto',
        ),
        migrations.RemoveField(
            model_name='proyecto',
            name='scrumMaster',
        ),
        migrations.RemoveField(
            model_name='proyecto',
            name='usuario_rol',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='flujo',
        ),
        migrations.DeleteModel(
            name='Flujo',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='proyecto',
        ),
        migrations.DeleteModel(
            name='Proyecto',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='sprint',
        ),
        migrations.DeleteModel(
            name='Sprint',
        ),
        migrations.RemoveField(
            model_name='user_story',
            name='user',
        ),
        migrations.DeleteModel(
            name='User_Story',
        ),
        migrations.RemoveField(
            model_name='usuario_rol',
            name='rol',
        ),
        migrations.RemoveField(
            model_name='usuario_rol',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Usuario_rol',
        ),
    ]
