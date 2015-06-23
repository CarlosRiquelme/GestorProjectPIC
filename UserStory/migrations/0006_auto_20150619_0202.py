# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0005_auto_20150619_0144'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userstory',
            old_name='suma_tiempo',
            new_name='suma_trabajadas',
        ),
    ]
