# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserStory', '0011_us_estado_ultimo_estado_actual'),
    ]

    operations = [
        migrations.CreateModel(
            name='prueba',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
