# Generated by Django 4.1.7 on 2024-02-23 12:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xpapp', '0042_alter_movimentacoesxp_data_movimentacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacoesxp',
            name='data_movimentacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 23, 9, 58, 15, 160917)),
        ),
    ]