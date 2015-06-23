# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Sprint', '0006_proyecto_en_proceso_sprint_en_proceso'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dias_de_un_Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dia', models.IntegerField(null=True)),
                ('fecha', models.DateField(null=True)),
                ('sprint', models.ForeignKey(to='Sprint.Sprint')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
