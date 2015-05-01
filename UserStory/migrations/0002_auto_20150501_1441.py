# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='estado',
            field=models.CharField(default=b'CREADO', max_length=30, choices=[(b'CREADO', b'CREADO'), (b'TODO', b'TODO'), (b'DOING', b'DOING'), (b'DONE', b'DONE')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userstory',
            name='priodidad',
            field=models.CharField(default=b'BAJA', max_length=30, null=True, choices=[(b'BAJA', b'BAJA'), (b'MEDIA', b'MEDIA'), (b'ALTA', b'ALTA')]),
            preserve_default=True,
        ),
    ]
