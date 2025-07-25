# Generated by Django 5.1.5 on 2025-07-15 13:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inicio', '0005_crearhorario_habitardeshabilitar_horariocita'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crearhorario',
            name='hora_final',
            field=models.TimeField(default='18:00', verbose_name='Hora de final'),
        ),
        migrations.AlterField(
            model_name='crearhorario',
            name='id_usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Medico'),
        ),
    ]
