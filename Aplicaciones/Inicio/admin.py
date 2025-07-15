from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.

class Admin_Contacto(admin.ModelAdmin):
    list_display = ['nombres', 'apellidos', 'telefono', 'motivo', 'mensaje', 'contactar', 'fecha_solicitud']
    
    class Meta:
        model = ContactarUsuario    


# Modelos enviados a panel de control de Django

admin.site.register(CreacionUser, UserAdmin) # Modelo personalizado de Usuario
admin.site.register(ContactarUsuario, Admin_Contacto)
#admin.site.register(RegistroUsuario)
