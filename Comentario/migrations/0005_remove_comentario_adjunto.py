# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0004_auto_20150502_0557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comentario',
            name='adjunto',
        ),
    ]
