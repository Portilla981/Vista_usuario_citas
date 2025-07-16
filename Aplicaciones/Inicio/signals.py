from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

@receiver(post_save, sender = CrearHorario)
def crear_intervalo_citas(sender, instance, created, **kwargs):
    if created:
        hora_inicial = instance.hora_inicio
        hora_final = instance.hora_final
        intervalo = timedelta(minutes= instance.duracion)
        print(intervalo)
        while hora_inicial < hora_final:
            
            HorarioCita.objects.create(
                horario = instance,
                fecha =  instance.fecha,
                hora_cita = hora_inicial,
                disponible = True               
            )
            hora_inicial = (datetime.combine(instance.fecha, hora_inicial)+ intervalo).time()
