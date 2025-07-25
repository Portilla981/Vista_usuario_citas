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
    path('sesion/listar/citas', citas_programadas, name='Citas_programadas'),
    path('sesion/listar/busqueda/', busquedaUser, name='Buscar_user'),
    path('sesion/listar/horarios/', listar_horarios_medicos, name='Lista_Horarios'),
    path('sesion/listar/horarios/buscar', buscar_citas, name='Buscar_Horarios'),
    path('sesion/listar/horarios/editar/<int:pk>/', editar_horario_medicos, name='Editar_Horarios'), # type: ignore
    
    path('sesion/perfil/', visualizar_cuenta, name='Perfiles'),
    path('sesion/cuenta/<int:pk>/', ver_cuentas, name='Perfil_Usuario'), # type: ignore
    path('sesion/cuenta/Editar/<int:pk>/', editar_cuenta, name='Perfil_Editar'), # type: ignore
    path('sesion/cuenta/horarios/', horarioCitas, name='Registro_horario'), # type: ignore
    path('sesion/cuenta/citas/', mostrar_horario_disponible, name='Registro_Citas'), # type: ignore
    path('sesion/cuenta/cita_asignada/', asignar_cita, name='Tomar_cita'), # type: ignore
    path('sesion/cuenta/mis_citas/', citas_usuario, name='Mis_citas'), # type: ignore
    path('sesion/cuenta/mis_citas/cancelar/<int:cita_id>/', cancelar_cita_usuario, name='Cancelar_citas'), # type: ignore

]
