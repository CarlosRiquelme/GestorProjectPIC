# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0006_auto_20150702_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='archivo',
        ),
    ]
