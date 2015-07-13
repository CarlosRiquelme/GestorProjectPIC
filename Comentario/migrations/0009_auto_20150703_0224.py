# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Comentario', '0008_auto_20150702_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archivo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bytes', models.TextField()),
                ('filename', models.CharField(max_length=255)),
                ('mimetype', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='document',
            name='docfile',
        ),
        migrations.AddField(
            model_name='document',
            name='archivo',
            field=models.FileField(null=True, upload_to=b'Comentario.Archivo/bytes/filename/mimetype', blank=True),
            preserve_default=True,
        ),
    ]
