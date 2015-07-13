# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0003_auto_20150530_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='archivo',
            field=models.FileField(default=1, upload_to=b''),
            preserve_default=False,
        ),
    ]
