# Generated by Django 4.1.7 on 2024-02-21 22:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informes_legais', '0007_movimentodetalhado_cotista_movimentodetalhado_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contaefin',
            name='data_final',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 21, 19, 48, 18, 628487)),
        ),
        migrations.AlterField(
            model_name='movimentodetalhado',
            name='data',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 21, 19, 48, 18, 632488)),
        ),
    ]