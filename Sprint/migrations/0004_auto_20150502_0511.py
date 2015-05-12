# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0003_sprint_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='tiempo_acumulado',
            field=models.IntegerField(default=0, null=True),
            preserve_default=True,
        ),
    ]
