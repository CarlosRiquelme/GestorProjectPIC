# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminProyectos', '0001_initial'),
        ('UserStory', '0003_auto_20150501_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='proyecto',
            field=models.ForeignKey(to='AdminProyectos.Proyecto', null=True),
            preserve_default=True,
        ),
    ]
