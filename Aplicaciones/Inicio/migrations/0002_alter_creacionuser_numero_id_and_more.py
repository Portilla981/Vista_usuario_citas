# Generated by Django 5.1.5 on 2025-07-07 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inicio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creacionuser',
            name='numero_id',
            field=models.PositiveBigIntegerField(default=0, help_text='Ingrese su numero de identificación', unique=True, verbose_name='Numero de identificación'),
        ),
        migrations.AlterField(
            model_name='creacionuser',
            name='telefono',
            field=models.PositiveBigIntegerField(default=0, help_text='Ingrese su numero de identificación', verbose_name='Teléfono'),
        ),
    ]
