# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0007_remove_document_archivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='comentario',
            field=models.ForeignKey(to='Comentario.Comentario'),
            preserve_default=True,
        ),
    ]
