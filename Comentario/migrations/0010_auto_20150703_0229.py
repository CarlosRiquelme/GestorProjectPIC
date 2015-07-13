# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0009_auto_20150703_0224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='archivo',
            new_name='docfile',
        ),
    ]
