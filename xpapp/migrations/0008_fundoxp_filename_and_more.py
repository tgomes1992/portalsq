# Generated by Django 4.1.7 on 2023-09-29 18:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xpapp', '0007_alter_movimentacoesxp_data_movimentacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundoxp',
            name='filename',
            field=models.CharField(default='XP', max_length=200),
        ),
        migrations.AlterField(
            model_name='movimentacoesxp',
            name='data_movimentacao',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 29, 15, 18, 48, 580087)),
        ),
    ]
