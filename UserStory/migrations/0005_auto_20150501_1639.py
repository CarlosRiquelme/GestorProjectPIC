# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0004_userstory_proyecto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userstory',
            old_name='priodidad',
            new_name='prioridad',
        ),
    ]
