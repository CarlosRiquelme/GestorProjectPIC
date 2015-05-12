# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PIC', '0003_rolusuarioproyecto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rolusuarioproyecto',
            name='rol',
            field=models.ForeignKey(to='auth.Group', null=True),
            preserve_default=True,
        ),
    ]
