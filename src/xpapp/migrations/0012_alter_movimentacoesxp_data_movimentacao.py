# Generated by Django 4.1.7 on 2023-12-06 14:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xpapp', '0011_alter_movimentacoesxp_data_movimentacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacoesxp',
            name='data_movimentacao',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 6, 11, 38, 13, 374861)),
        ),
    ]