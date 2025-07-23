from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


# Función de creación los intervalos del horario por medio de un lanzador o señal de post
@receiver(post_save, sender = CrearHorario)
def crear_intervalo_citas(sender, instance, created, **kwargs):
    
    hora_inicial = instance.hora_inicio
    hora_final = instance.hora_final
    intervalo = timedelta(minutes= instance.duracion) 
    print(f'Se divide por {intervalo} minutos')     
    
    if created:       
        
        while hora_inicial < hora_final:
            
            HorarioCita.objects.create(
                horario = instance,
                fecha =  instance.fecha,
                hora_cita = hora_inicial,
                #disponible = True               
            )
            
            hora_inicial = (datetime.combine(instance.fecha, hora_inicial)+ intervalo).time()

        print(f'Se creo el horario de {instance.id_usuario}')
        
    else:
        
        print('Entrando Intervalos de edición')        
        valor = UsuarioCitas.objects.filter(usuario = instance.id_usuario, cita = instance.id)
        
        print(valor)         # type: ignore
        if valor.exists():            
            valor.delete()
            print('Hubo necesidad de borrar')        
        else:
            
            print('vacio')
        
        while hora_inicial < hora_final:
            
            HorarioCita.objects.create(
                horario = instance,
                fecha =  instance.fecha,
                hora_cita = hora_inicial,
                #disponible = True               
            )
            
            hora_inicial = (datetime.combine(instance.fecha, hora_inicial)+ intervalo).time()

        print(f'Se creo el horario de {instance.id_usuario}')
        