# Generated by Django 4.1.7 on 2024-03-05 16:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xpapp', '0048_alter_movimentacoesxp_data_movimentacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacoesxp',
            name='data_movimentacao',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 5, 13, 33, 30, 770306)),
        ),
    ]