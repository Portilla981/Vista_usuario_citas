"""
URL configuration for Plataforma_Medica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Ruta de las urls propias 
    path('', include('Aplicaciones.Inicio.url_Inicio')),
    # path('AdminS/', include('Administrador.url_Administrador')),
    # path('Medico/', include('Medico.url_Medico')),
    # path('Usuario/', include('Paciente.url_Paciente')),    
    # path('Recepcion/', include('Recepcion.url_Recepcion')),
    
]
