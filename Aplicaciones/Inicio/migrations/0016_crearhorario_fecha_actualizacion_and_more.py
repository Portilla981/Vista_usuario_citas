# Generated by Django 5.2.3 on 2025-07-23 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inicio', '0015_usuariocitas_estado_cita'),
    ]

    operations = [
        migrations.AddField(
            model_name='crearhorario',
            name='fecha_actualizacion',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='habitardeshabilitar',
            name='fecha_hora',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
