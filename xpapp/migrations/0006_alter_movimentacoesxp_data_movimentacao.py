# Generated by Django 4.1.7 on 2023-09-08 16:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xpapp', '0005_alter_arquivosxp_filename_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimentacoesxp',
            name='data_movimentacao',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 8, 13, 53, 16, 982179)),
        ),
    ]
