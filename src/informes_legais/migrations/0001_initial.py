# Generated by Django 4.1.7 on 2024-02-15 20:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseMovimentacoes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('cd_tipo', models.CharField(default=' ', max_length=20)),
                ('cd_jcot', models.TextField()),
                ('cotista', models.TextField()),
                ('vl_original', models.FloatField()),
                ('vl_liquido', models.FloatField()),
                ('vl_bruto', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ContaEfin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creditos', models.FloatField()),
                ('debitos', models.FloatField()),
                ('creditosmsmtitu', models.FloatField()),
                ('debitosmsmtitu', models.FloatField()),
                ('vlrultidia', models.FloatField()),
                ('fundoCnpj', models.CharField(max_length=14)),
                ('numconta', models.TextField(max_length=14)),
                ('data_final', models.DateTimeField(default=datetime.datetime(2024, 2, 15, 17, 1, 10, 737296))),
            ],
        ),
        migrations.CreateModel(
            name='InvestidorEfin',
            fields=[
                ('nome', models.CharField(default='', max_length=256)),
                ('cpfcnpj', models.CharField(default='', max_length=14, primary_key=True, serialize=False)),
                ('endereco', models.TextField(default='', max_length=256)),
                ('pais', models.TextField(default='', max_length=5)),
                ('data_final', models.DateTimeField(default=datetime.datetime(2024, 2, 15, 17, 1, 10, 738296))),
            ],
        ),
    ]
