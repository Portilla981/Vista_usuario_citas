from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

# seccion de creacion las vistas de los modelos en el administrador de django
class Admin_Contacto(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'telefono', 'motivo', 'mensaje', 'contactar', 'fecha_solicitud']
    
    class Meta:
        model = ContactarUsuario    

class CreacionUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'tipo_usuario', 'fecha_actualizacion', 'nombre_completo', 'cambiar_contrasena']
    fieldsets = (
        (None, {
            'fields': ('tipo_id', 'first_name', 'last_name','numero_id', 'telefono', 'tipo_usuario', 'cambiar_contrasena')
        }),
    )   
    search_fields = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['tipo_usuario', 'cambiar_contrasena']
    ordering = ['-id']
    
class CitasAdmin(admin.ModelAdmin):
    list_display = [ 'fecha', 'hora_cita', 'estado', 'asistencia']
    fieldsets = (
        (None, {
            'fields': ( 'fecha', 'hora_cita', 'estado', 'asistencia')
        }),
    )
    search_fields = ['medico__username', 'fecha']
    list_filter = ['estado', 'asistencia']
    ordering = ['fecha', 'hora_cita']
    
class HorarioCitaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'cita', 'fecha_registro']
    fieldsets = (
        (None, {
            'fields': ('usuario', 'cita')
        }),
    )
    search_fields = ['usuario__nombre_completo']
    list_filter = ['cita__estado']
    ordering = ['usuario', 'cita']
    
class CrearHorarioAdmin(admin.ModelAdmin):
    list_display = ['id_usuario', 'fecha', 'hora_inicio', 'hora_final', 'duracion', 'fecha_registro', 'fecha_actualizacion']
    fieldsets = (
        (None, {
            'fields': ('id_usuario', 'fecha', 'hora_inicio', 'hora_final', 'duracion')
        }),
    )
    search_fields = ['id_usuario__nombre_completo', 'fecha']
    list_filter = ['id_usuario__tipo_usuario']
    ordering = ['fecha_registro']
    
class HistoriaClinicaAdmin(admin.ModelAdmin):
    list_display = ['id_cita', 'fecha_registro', 'fecha_actualizacion', 'motivo_consulta', 'diagnostico', 'tratamiento']
    fieldsets = (
        (None, {
            'fields': ('id_cita', 'motivo_consulta', 'diagnostico', 'tratamiento')
        }),
    )
    search_fields = ['id_cita__usuario__nombre_completo']
    list_filter = ['id_cita__usuario__tipo_usuario']
    ordering = ['fecha_registro']



# Modelos enviados a panel de control de Django
admin.site.register(CreacionUser, CreacionUserAdmin) # Modelo personalizado de Usuario
admin.site.register(ContactarUsuario, Admin_Contacto)
admin.site.register(UsuarioCitas, HorarioCitaAdmin)
admin.site.register(HorarioCita, CitasAdmin)
admin.site.register(CrearHorario, CrearHorarioAdmin)
admin.site.register(HistoriaClinica, HistoriaClinicaAdmin)

