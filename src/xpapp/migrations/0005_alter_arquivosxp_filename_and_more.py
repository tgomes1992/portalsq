# Generated by Django 4.1.7 on 2023-06-29 18:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xpapp', '0004_alter_fundoxp_categoria_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arquivosxp',
            name='filename',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='movimentacoesxp',
            name='data_movimentacao',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 29, 15, 28, 58, 165421)),
        ),
        migrations.AlterField(
            model_name='movimentacoesxp',
            name='filename',
            field=models.CharField(max_length=400),
        ),
    ]