# Generated by Django 4.1.7 on 2024-01-18 19:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqdados', '0007_receitamensal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receitamensal',
            name='valor_remuneracao',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
