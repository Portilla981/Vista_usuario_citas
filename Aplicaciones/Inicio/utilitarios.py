from datetime import datetime, timedelta
from .models import *

#Crear funcion de division de horarios 
def division_horario(horario_medico):
    
    intervalos = []
    print(horario_medico)
    hora_inicial = horario_medico.hora_inicio
    print(hora_inicial)
    duracion_cita = timedelta(minutes=horario_medico.duracion) 
    print(duracion_cita)
    while hora_inicial < horario_medico.hora_final:
        hora_finalizacion = (datetime.combine(horario_medico.fecha, hora_inicial)+ duracion_cita).time()
        print(hora_finalizacion)
        division = HorarioCita(  # type: ignore
            horario = horario_medico,
            hora_inicio = hora_inicial,
            hora_fin = hora_finalizacion,
            disponible=True           
        )
        intervalos.append(division)
        hora_inicial = hora_finalizacion
    HorarioCita.objects.bulk_create(intervalos)
        
        
        
    # def dividir_horario(horario_medico):
    # intervalos = []
    # hora_inicio = horario_medico.hora_inicio
    # duracion_consulta = timedelta(minutes=horario_medico.duracion_consulta)
    # while hora_inicio < horario_medico.hora_fin:
    #     hora_fin = (datetime.combine(horario_medico.fecha, hora_inicio) + duracion_consulta).time()
    #     intervalo = IntervaloHorario(
    #         horario_medico=horario_medico,
    #         hora_inicio=hora_inicio,
    #         hora_fin=hora_fin,
    #         disponible=True
    #     )
    #     intervalos.append(intervalo)
    #     hora_inicio = hora_fin
    # IntervaloHorario.objects.bulk_create(intervalos)
