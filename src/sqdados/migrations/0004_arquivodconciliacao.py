# Generated by Django 4.1.7 on 2023-12-08 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sqdados', '0003_cdot'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArquivoDconciliacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_ativo', models.CharField(max_length=25)),
                ('ativo', models.CharField(max_length=25)),
                ('data', models.DateTimeField()),
                ('quantidade', models.FloatField()),
            ],
        ),
    ]
