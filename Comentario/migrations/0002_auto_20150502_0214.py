# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='adjunto',
            field=models.FileField(null=True, upload_to=b'documents/%Y%m%d'),
            preserve_default=True,
        ),
    ]
