# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Flujo', '0002_flujo_estado'),
        ('Sprint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='flujo',
            field=models.ForeignKey(to='Flujo.Flujo', null=True),
            preserve_default=True,
        ),
    ]
