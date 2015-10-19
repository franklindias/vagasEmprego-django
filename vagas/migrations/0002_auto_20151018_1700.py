# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaga',
            name='enderecoImagem',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vaga',
            name='dataAbertura',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
