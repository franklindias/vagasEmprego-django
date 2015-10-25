# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vagas', '0002_auto_20151018_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='candidato',
            name='areaAtuacao',
            field=models.CharField(null=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='candidato',
            name='formacao',
            field=models.CharField(null=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='candidato',
            name='sexo',
            field=models.CharField(null=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='vagatemcandidatos',
            name='aprovado',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='vagatemcandidatos',
            name='dataCandidatura',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
