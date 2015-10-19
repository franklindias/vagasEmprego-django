# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formacao', models.CharField(max_length=30)),
                ('areaAtuacao', models.CharField(max_length=30)),
                ('sexo', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Endereco',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logradouro', models.CharField(max_length=50)),
                ('bairro', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=50)),
                ('cep', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoUser', models.CharField(max_length=9)),
                ('nomeCompleto', models.CharField(max_length=30)),
                ('endereco', models.ForeignKey(to='vagas.Endereco')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vaga',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataAbertura', models.DateField()),
                ('dataFechamento', models.DateField()),
                ('salario', models.DecimalField(max_digits=8, decimal_places=2)),
                ('cargaHoraria', models.CharField(max_length=25)),
                ('funcao', models.CharField(max_length=100)),
                ('descricao', models.CharField(max_length=255)),
                ('empresa', models.ForeignKey(to='vagas.Empresa')),
            ],
        ),
        migrations.CreateModel(
            name='VagaTemCandidatos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataCandidatura', models.DateField()),
                ('aprovado', models.BooleanField()),
                ('candidato', models.ForeignKey(to='vagas.Candidato')),
                ('vaga', models.ForeignKey(to='vagas.Vaga')),
            ],
        ),
        migrations.AddField(
            model_name='empresa',
            name='usuario',
            field=models.ForeignKey(to='vagas.Usuario'),
        ),
        migrations.AddField(
            model_name='candidato',
            name='usuario',
            field=models.ForeignKey(to='vagas.Usuario'),
        ),
    ]
