from django.urls import path
from .views import *

#app_name = 'Inicio'

urlpatterns = [
    path('', inicio_proceso, name='Inicio'),
    path('about/', nosotros, name='Nosotros'),
    path('contactar/', contactarU, name='Contactar'),
    path('sesion/Login', iniciar_sesion, name='Inicio_sesion'),  # type: ignore
    path('sesion/inicio', ingreso_principal, name='Principal'),
    path('sesion/crear/', registro_usuario, name='Registro_usuario'),  # type: ignore
    path('sesion/logout/', salir_sesion, name='Sesion_Cerrada'),
    path('sesion/listar/', listar_cuentas, name='Lista_cuentas'),
    #path('sesion/listar/', CuentasListView, name='Lista_cuentas_class'), # type: ignore
    path('sesion/perfil/', visualizar_cuenta, name='Perfiles'),
    path('sesion/cuenta/<int:pk>/', ver_cuentas, name='Perfil_Usuario'), # type: ignore
    path('sesion/cuenta/Editar/<int:pk>/', editar_cuenta, name='Perfil_Editar'), # type: ignore
    path('sesion/cuenta/horarios', horarioCitas, name='Registro_horario'), # type: ignore

]
