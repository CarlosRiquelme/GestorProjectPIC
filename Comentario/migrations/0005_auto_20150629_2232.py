# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0004_comentario_archivo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='archivo',
        ),
        migrations.AddField(
            model_name='document',
            name='archivo',
            field=models.FileField(default=1, upload_to=b''),
            preserve_default=False,
        ),
    ]
