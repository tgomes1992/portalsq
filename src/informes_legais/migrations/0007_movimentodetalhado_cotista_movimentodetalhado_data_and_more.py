# Generated by Django 4.1.7 on 2024-02-21 22:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informes_legais', '0006_movimentodetalhado_alter_contaefin_data_final'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimentodetalhado',
            name='cotista',
            field=models.CharField(default='', max_length=14),
        ),
        migrations.AddField(
            model_name='movimentodetalhado',
            name='data',
            field=models.CharField(default='', max_length=14),
        ),
        migrations.AlterField(
            model_name='contaefin',
            name='data_final',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 21, 19, 45, 50, 576698)),
        ),
    ]