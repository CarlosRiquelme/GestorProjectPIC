# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import Comentario.models


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0003_auto_20150502_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='adjunto',
            field=models.FileField(null=True, upload_to=Comentario.models.url),
            preserve_default=True,
        ),
    ]
