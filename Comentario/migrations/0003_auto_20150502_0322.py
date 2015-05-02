# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0002_auto_20150502_0214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='adjunto',
            field=models.FileField(null=True, upload_to=b'documents'),
            preserve_default=True,
        ),
    ]
