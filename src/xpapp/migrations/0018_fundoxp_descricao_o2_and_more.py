# Generated by Django 4.1.7 on 2024-01-05 15:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xpapp', '0017_alter_movimentacoesxp_data_movimentacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundoxp',
            name='descricao_o2',
            field=models.CharField(default=' ', max_length=400),
        ),
        migrations.AlterField(
            model_name='movimentacoesxp',
            name='data_movimentacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 5, 12, 27, 48, 106177)),
        ),
    ]