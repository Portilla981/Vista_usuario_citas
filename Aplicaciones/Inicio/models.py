from django.db import models
from django.utils import timezone
from datetime import datetime
# creación de la tabla de usuario d django extendida
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from .utilitarios import *


# Creación de usuarios
class CreacionUser(AbstractUser):  
    # Variables o lista de opciones, verificar cambios antes de actualizar   
    class Tipo_User(models.TextChoices):        
        ADMIN = 'Administrador',
        PACIENTE = 'Paciente'
        MEDICO = 'Medico'
        RECEPCION = 'Recepcionista'
        
    class Tipo_id(models.TextChoices):
        CEDULA = 'Cédula'
        TARJETA_ID= 'Tarjeta Identidad'
        CED_EXT = 'Cédula Extranjería'
        PASAPORTE = 'Pasaporte'
        
        
    tipo_id = models.CharField( max_length=20 ,choices = Tipo_id.choices, default = Tipo_id.CEDULA, verbose_name='Tipo de documento'  )
    numero_id = models.PositiveBigIntegerField(null=False, blank=False,  verbose_name='Numero de identificación', unique=True, default=0)
    telefono = models.PositiveBigIntegerField(null= False, blank= False, verbose_name='Teléfono', default=0)
    tipo_usuario = models.CharField(max_length=20, choices = Tipo_User.choices, default = Tipo_User.PACIENTE, verbose_name='Tipo Usuario')    
    fecha_actualizacion = models.DateTimeField (auto_now=True, verbose_name='Ultima Actualización')
    nombre_completo= models.CharField(max_length = 100, null=False, blank= False, verbose_name='Nombre completo') 
    cambiar_contrasena = models.BooleanField(default=True, verbose_name='Cambiar contraseña')  
    
    # Función automática para formar el nombre completo al crear el usuario 
    def save(self, *args, **kwargs):
        self.nombre_completo = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)    

# Registro de habilitación y deshabilitación de usuarios
class HabilitarDeshabilitar(models.Model):    
    id_usuario = models.ForeignKey(CreacionUser, on_delete= models.CASCADE)
    motivo = models.CharField(max_length= 255, null=False, blank=False)
    estado = models.CharField(max_length= 20, null=False, blank=False)    
    fecha_hora = models.DateTimeField(auto_now_add=True)
    
# Creación de horarios del medico y su iteracion por medio de una señal
class CrearHorario(models.Model):
    id_usuario = models.ForeignKey(CreacionUser, on_delete= models.CASCADE, verbose_name='Medico')
    fecha = models.DateField(null=False, blank=False, verbose_name='Fecha de horario')
    hora_inicio = models.TimeField(null=False, blank=False, default= '08:00', verbose_name='Hora de inicio')# type: ignore
    hora_final = models.TimeField(null=False, blank=False, default= '18:00', verbose_name='Hora de final') # type: ignore
    duracion = models.IntegerField(null=False, blank=False, default= 20, verbose_name='Duración de Cita')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
        
# Clase para crear los horarios de citas segun el horario del medico    
class HorarioCita(models.Model):
    
    class Estado(models.TextChoices):
        DISPONIBLE = 'Disponible'
        AGENDADA = 'Agendada'
        REPROGRAMADA = 'Reprogramada'
        CANCELADA = 'Cancelada'  
    
    class Asistencia(models.TextChoices):
        ASISTIO = 'Asistio'
        NO_ASISTIO = 'No asistio'
        ESPERA = 'A la espera'
        
    horario = models.ForeignKey(CrearHorario, on_delete= models.CASCADE)
    fecha = models.DateField(verbose_name='Fecha')
    hora_cita = models.TimeField(verbose_name='Hora de inicio')    
    estado = models.CharField(max_length=20, choices = Estado.choices, default= Estado.DISPONIBLE, verbose_name='Estado')   
    asistencia = models.CharField(max_length=20, choices = Asistencia.choices, default= Asistencia.ESPERA, verbose_name='Asistencia')   
    
# asignación de citas a los usuarios
class UsuarioCitas(models.Model):
    usuario = models.ForeignKey(CreacionUser, on_delete= models.CASCADE, verbose_name='Usuario')
    cita = models.ForeignKey(HorarioCita, on_delete= models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    actividad_cita = models.CharField(max_length=20, default= "Asignada", verbose_name='Estado Cita')
    
# Creación de historia clínica
class HistoriaClinica(models.Model):
    id_cita = models.ForeignKey(UsuarioCitas, on_delete=models.CASCADE, verbose_name='Cita asignada')
    motivo_consulta = models.TextField(max_length=500, null=False, blank=False, verbose_name='Motivo de consulta')
    diagnostico = models.TextField(max_length=500, null=False, blank=False, verbose_name='Diagnóstico')
    tratamiento = models.TextField(max_length=500, null=False, blank=False, verbose_name='Tratamiento')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Consulta')
    fecha_actualizacion = models.DateTimeField(auto_now=True)

# Creación de formulario para contactarse
class ContactarUsuario(models.Model):
    class Motivo(models.TextChoices):
        GENERAL = 'General'
        CITAS = 'Citas'
        RESULTADOS = 'Resultados'
        MANUAL = 'Manual de usuario'
        
    class ContatarM(models.TextChoices):
        TELEFONO = 'Teléfono'
        EMAIL = 'Correo Electrónico'
    
    nombres = models.CharField(max_length = 50, null=False, blank= False, verbose_name='Nombres')
    apellidos = models.CharField(max_length = 50, null= False, blank= False, verbose_name='Apellidos')
    email = models.EmailField(max_length=255, null= False, blank= False, verbose_name='Correo Electronico')
    telefono = models.BigIntegerField(null= False, blank= False, verbose_name='Teléfono')
    motivo = models.CharField(max_length=20, choices = Motivo.choices, verbose_name='Motivo')
    mensaje = models.TextField(max_length=200, null= False, blank= False, verbose_name='Mensaje')
    contactar = models.CharField(max_length=20, choices = ContatarM.choices, verbose_name='Medio de contacto')   
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']        
    
    def __str__(self):
        return f'{self.nombres} - {self.apellidos}' 

















