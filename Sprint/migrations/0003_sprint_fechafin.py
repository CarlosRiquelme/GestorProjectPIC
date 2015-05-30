# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0002_auto_20150529_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='fechaFin',
            field=models.DateField(null=True),
            preserve_default=True,
        ),
    ]
