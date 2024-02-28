# Generated by Django 4.1.7 on 2024-02-21 22:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informes_legais', '0005_resgatesjcot_alter_contaefin_data_final'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimentoDetalhado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notaOperacao', models.CharField(max_length=100)),
                ('notaAplicacao', models.CharField(max_length=100)),
                ('dsFormaLiquidacao', models.CharField(max_length=100)),
                ('tpLiquidacao', models.CharField(max_length=100)),
                ('dsContaLiquidacao', models.CharField(max_length=100)),
                ('qtdCotas', models.FloatField()),
                ('vlOriginal', models.FloatField()),
                ('vlOperacao', models.FloatField()),
                ('vlIR', models.FloatField()),
                ('vlPenaltyFee', models.FloatField()),
                ('vlReceitaSaqueCarencia', models.FloatField()),
                ('vlIOF', models.FloatField()),
                ('vlLiquido', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='contaefin',
            name='data_final',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 21, 19, 42, 25, 984444)),
        ),
    ]
