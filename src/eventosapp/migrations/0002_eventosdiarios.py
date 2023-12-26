# Generated by Django 4.1.7 on 2023-12-06 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventosapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventosDiarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.CharField(max_length=200)),
                ('emissor', models.CharField(max_length=250)),
                ('data_base', models.DateTimeField()),
                ('data_liquidacao', models.DateTimeField()),
            ],
        ),
    ]
