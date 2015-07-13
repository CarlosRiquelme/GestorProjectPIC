# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0008_auto_20150629_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='suma_trabajadas',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='tiempo_estimado',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
