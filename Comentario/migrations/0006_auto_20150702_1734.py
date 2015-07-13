# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0005_auto_20150629_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='comentario',
            field=models.ForeignKey(to='Comentario.Comentario', null=True),
            preserve_default=True,
        ),
    ]
