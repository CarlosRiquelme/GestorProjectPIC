# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0001_initial'),
        ('UserStory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comentario',
            name='userstory',
            field=models.ForeignKey(to='UserStory.UserStory', null=True),
            preserve_default=True,
        ),
    ]
