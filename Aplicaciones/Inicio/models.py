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
    
    def save(self, *args, **kwargs):
        self.nombre_completo = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)    
    

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
    fecha_solicitud = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    class Meta:
        ordering = ['-id']        
    
    def __str__(self):
        return f'{self.nombres} - {self.apellidos}' 
    
    
class HabitarDeshabilitar(models.Model):    
    id_usuario = models.ForeignKey(CreacionUser, on_delete= models.CASCADE)
    motivo = models.CharField(max_length= 255, null=False, blank=False)    
    fecha_hora = models.DateTimeField()
    

class CrearHorario(models.Model):
    id_usuario = models.ForeignKey(CreacionUser, on_delete= models.CASCADE, verbose_name='Medico')
    fecha = models.DateField(null=False, blank=False, verbose_name='Fecha de horario')
    hora_inicio = models.TimeField(null=False, blank=False, default= '08:00', verbose_name='Hora de inicio')# type: ignore
    hora_final = models.TimeField(null=False, blank=False, default= '18:00', verbose_name='Hora de final') # type: ignore
    duracion = models.IntegerField(null=False, blank=False, default= 20, verbose_name='Duracion de Cita')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
            
class HorarioCita(models.Model):
    horario = models.ForeignKey(CrearHorario, on_delete= models.CASCADE)
    fecha = models.DateField(verbose_name='Fecha')
    hora_cita = models.TimeField(verbose_name='Hora de inicio')# type: ignore    
    disponible = models.BooleanField(default=True)
    



# Cracion de otro modelo de usuarios 
'''class RegistroUsuario(models.Model):
    nombres = models.CharField(max_length=50, null = False, blank = False, verbose_name='Nombres:')
    apellidos = models.CharField(max_length=50, null = False, blank = False, verbose_name='Apellidos:')
    telefono = models.BigIntegerField(null = False, blank = False, verbose_name='Teléfono:')
    email = models.EmailField(unique=True, max_length=255, null = False, blank = False, verbose_name='Correo Electrónico:')
    tipo_usuario = models.IntegerField(choices = OPC_TIPO_USU, default = 0, verbose_name='Tipo Usuario:')
    fecha_nacimiento= models.DateField(default=datetime.now, verbose_name='Fecha de Nacimiento')
    nombre_usuario = models.CharField(max_length=20, null = False, blank = False, verbose_name='Nombre Usuario:')
    fecha_creacion= models.DateField(auto_now=True, verbose_name='Fecha de Creacion')
    hora_creacion=models.TimeField(auto_now=True, verbose_name='Hora de Creacion')
    ultimo_acceso =  models.DateTimeField(auto_now_add=True, verbose_name='Ultimo ingreso')        
    passwor_1 = models.CharField(max_length=20,  null = False, blank = False, verbose_name='Contraseña')
    passwor_2 = models.CharField(max_length=20,  null = False, blank = False, verbose_name='Repita Contraseña')    
    estado = models.BooleanField(default= True, verbose_name= 'Estado Usuario')
    
        
    class Meta:
        ordering = ['-id'] 
        
    def __str__(self):
        return f'{self.nombres} - {self.apellidos} '   '''
    
    




