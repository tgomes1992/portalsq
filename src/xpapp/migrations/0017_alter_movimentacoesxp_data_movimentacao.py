# Generated by Django 4.1.7 on 2024-01-03 20:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xpapp', '0016_alter_movimentacoesxp_data_movimentacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacoesxp',
            name='data_movimentacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 3, 17, 5, 3, 857906)),
        ),
    ]
