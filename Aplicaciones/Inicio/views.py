from django.contrib import messages
# from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .forms import *
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import *  # type: ignore
from django.contrib.auth.decorators import *  # type: ignore
#from django.http import HttpResponse
from django.views.generic import ListView
from django.db.models import F, Value
from django.db.models.functions import Concat



# Create your views here.
# Inicio
def inicio_proceso(request):
    titulo = 'Inicio'
    return render(request, 'paginas/inicio.html', {
        'titulo': titulo
    })

# Formulario de contactar
def contactarU(request):
    data = {
        'titulo': 'Contáctenos',
        'form': Formato_Contacto()
    }

    if request.method == 'GET':
        print('Ingreso a formulario de contacto')
        return render(request, 'paginas/contacto.html', data)
    else:
        print('Entrando método POST')
        try:
            formulario = Formato_Contacto(data=request.POST)
            print('Creando el formulario')
            if formulario.is_valid():
                print('Validacion de datos Exitosa')
                formulario.save()
                print('Enviando la solicitud')
                data['mensaje'] = 'Mensaje enviado'

        except ValueError:
            return render(request, 'contacto.html', {
                'form': Formato_Contacto,
                'error': 'Por favor ingrese datos validos',
            })
    return redirect('/')

# Vista de Nosotros
def nosotros(request):
    titulo = 'Nosotros'
    return render(request, 'paginas/nosotros.html', {
        'titulo': titulo
    })

# Login formato de inicio de sesión
def iniciar_sesion(request):
    if request.method == 'POST':
        print('Proceso de ingreso a sesión')
        formulario = Iniciar_Sesion(request.POST)
        print('Se crea data')
        if formulario.is_valid():
            print('Validación de datos')
            datos = formulario.cleaned_data
            print('Limpiando datos')
            usuario = authenticate(request, username = datos['usuario'], password = datos['password'])
            print('Método de autenticación')
            if usuario is not None:
                print(f'Existe el usuario {usuario}')
                if usuario.is_active:
                    print('Segunda confirmación')
                    login(request, usuario)
                    print('Ingreso exitoso')
                    return redirect('Principal')

                else:
                    print('Problemas de ingreso de segunda validación')
                    data = {
                        'titulo': 'Inicio Sesión',
                        'form': formulario,
                        'error': 'El Usuario no esta activo'
                    }
                    return render(request, 'paginas/iniciar_sesion.html', data)
            else:
                print('Problemas de ingreso de validación')
                data = {
                    'titulo': 'Inicio Sesión',
                    'form': formulario,
                    'error': 'Usuario o contraseña incorrect@, por favor verifique e intente nuevamente'
                }
                print('No se puede ingresar')
                # , HttpResponse('Usuario NO  encontrado')
                return render(request, 'paginas/iniciar_sesion.html', data)

    else:
        print('Ingresando a iniciar sesion')
        formulario = Iniciar_Sesion()
        data = {
            'titulo': 'Inicio Sesión',
            'form': formulario
        }
        return render(request, 'paginas/iniciar_sesion.html', data)

# Pagina de inicio de sesión
@login_required
def ingreso_principal(request):
    # data = [ titulo = 'Nosotros' ]
    titulo = 'Bienvenido'
    return render(request, 'sesiones/inicio_ingreso.html', {
        'titulo': titulo
    })

# Creación de usuarios
@login_required  
def registro_usuario(request):
    if request.method == 'POST':
        print('Envió de datos')
        form = Formato_RegistroU(request.POST)
        print('Se creo la data')
        if form.is_valid():
            print('Se verifica su validación')
            form.save()  # Guarda la contraseña y demás campos
            print('Usuario guardado ')
            messages.success(request, 'El usuario ha sido creado')
            return redirect('Principal')
        else:
            print('Ocurrió algún error')
            messages.error(request, 'Verifica los datos del formulario')
            return redirect('Registro_usuario')
    else:
        print('Se ingresa para crear usuario')
        form = Formato_RegistroU()
        
    return render(request, 'sesiones/sesion_usuario.html', {'form': form})


# Logout
@login_required
def salir_sesion(request):
    logout(request)
    return redirect('Inicio')


# listar 
@login_required
def listar_cuentas(request):
    data = {
        'titulo':'Listado de cuentas',
        'cuentas': CreacionUser.objects.filter(is_superuser = False)
    }        
    return render(request, 'paginas/listado_tabla.html', data)


@login_required
def visualizar_cuenta(request):
    print('Visualizando perfil')
    perfil = get_object_or_404(CreacionUser, username = request.user)    
    data = {
        'titulo':'Tu perfil',
        'admin': request.user,
        'perfil': perfil,
        'form': PerfilUsuario(instance = perfil)
    } 
    
    return render(request, 'paginas/mi_perfil.html', data)


@login_required # type: ignore
def ver_cuentas(request,pk):    
    perfil = get_object_or_404(CreacionUser, pk=pk)
    accion = request.GET.get('accion')    
    if accion == 'ver':    
        print(f'Viendo el perfil de {perfil.nombre_completo}')
        admin = request.user    
        form = PerfilUsuario(instance=perfil)             
        data = {
            'admin': admin,
            'perfil': perfil,
            'titulo':'Perfil',
            'form': form        
        }
        return render(request, 'paginas/mi_perfil.html', data)
    
    elif accion == 'habilitar':
        print(f'Estado {perfil.is_active}')
        if perfil.is_active == True :
            perfil.is_active = False
            #perfil.save()    
        else:
            perfil.is_active = True        
            #perfil.save() 
        perfil.save() 
        return redirect(reverse('Lista_cuentas')) 
        
    return render(request, 'paginas/listado_tabla.html')
            
    
@login_required # type: ignore
def editar_cuenta(request, pk):
    print("estamos jodidos")
    if request.method == 'GET':
        cuenta = get_object_or_404(CreacionUser, pk=pk)        
        admin = request.user  
        print(admin.username)    
        form2 = PerfilUsuario(instance=cuenta)   
        form = EditarUsuario(instance=cuenta)  
        data = {
            'perfil': cuenta,
            'admin': admin,
            'titulo':'Editar perfil',
            'form': form,
            'form2':form2        
        }
        return render(request, 'paginas/perfil.html', data)
    else:
        try:
            perfil = get_object_or_404(CreacionUser, pk=pk)
            form = EditarUsuario(request.POST, instance=perfil)
            
            if form.is_valid():
                print('Se verifica su validación')
                form.save() 
                return redirect(reverse('Perfil_Usuario', pk))

        except ValueError:
            return render(request, 'paginas/perfil.html', {
                'cuenta': perfil,
                'form': form,
                'error': "error al actualizar datos",
            })

# etsoy rewalizando barra de busqueda d evalores aqui vamosssssss
def  buscador(request):
    formato = BarraBusqueda()
    resultado = CreacionUser.objects.all()
    if request.GET.get('buscar'):
        formato = BarraBusqueda(request.GET)
        if formato.is_valid():
            buscar = formato.cleaned_data['buscar']
            resultado =CreacionUser.objects.filter(nombre_incontains=buscar)
    return render(request, 'buscador_html',{'formB': formato, 'resultsdo': resultado})
    
    
@login_required
def horarioCitas(request):
    if request.method == 'POST':
        print('Envio horario')        
        form = CreacionHorarioCitas(request.POST, usuario_actual = request.user)        
        if form.is_valid():
            print('guardando')            
            form.save()
            return redirect('Principal')        
    else:
        print('Generando')
        form = CreacionHorarioCitas(usuario_actual = request.user)
                
    return render(request, 'paginas/horarios.html', {'horario':form})

@login_required
def listar_horarios_medicos(request):    
    data = {
        'titulo':'Listado de cuentas',
        'horarioMed': CrearHorario.objects.all()
    }
    return render(request, 'sesiones/listar_horarios.html', data)
    
@login_required # type: ignore
def editar_horario_medicos(request, pk):
    print('Entrando a editar horario medico')
    horaId = get_object_or_404(CrearHorario, pk=pk) 
    medico= horaId.id_usuario
    if request.method == 'GET':        
        admin = request.user  
        print(admin.username) 
        print(f'Horario # {horaId.pk}')         
        # form2 = PerfilUsuario(instance=cuenta)   
        form = Formato_editar_horario(instance=horaId, initial={'id_usuario': medico.nombre_completo, 'fecha': horaId.fecha})  
        data = {
            'perfil': horaId,
            'admin': admin,            
            'formato': form,
            'medico':medico                
        }
        return render(request, 'sesiones/editar_horario.html', data)
    else:
        try:
            horaId = get_object_or_404(CrearHorario, pk=pk) 
            print(f'Entrando a Grabar {horaId.pk}' )
            # perfil = get_object_or_404(CrearHorario, pk=pk)
            form = Formato_editar_horario(request.POST, instance= horaId)
            
            if form.is_valid():                
                print('Se verifica su validación')
                form.save() 
                print('Se grabo exitosamente')
                return redirect('Lista_Horarios')
            else:
                print('NO se puede')
                

        except ValueError:
            return render(request, 'sesiones/editar_horario.html', {
                'cuenta': horaId,
                'formato': form,
                'error': "error al actualizar datos",
            })

    

# Listar las citas disponibles
@login_required
def mostrar_horario_disponible(request):  
    hoy = date.today()  
    medicos = CrearHorario.objects.all()
    # Filtros para la vista mayor que __gt menor q __lt mayor igual q  __gte menoir igual q __lte el dia de hoy
    intervalos = HorarioCita.objects.filter(fecha__gte = hoy).order_by('fecha') # type: ignore
        
    return render(request, 'paginas/horario_citas.html', {'tabla':intervalos, 'medico': medicos})
    
# Tomar cita por el usuario 
@login_required # type: ignore
def asignar_cita(request):
    print('Ingresando asignación')
    if request.method == 'POST':
        print('estamos validando')
        id_horario = request.POST.get('cita_horario') # type: ignore
        horario = HorarioCita.objects.get(id = id_horario)
        if horario.estado == 'Disponible':            
            print(horario.fecha)
            print(horario.id) # type: ignore
            horario.estado = 'Agendada' # type: ignore
            horario.save()
            cita_disponible = UsuarioCitas.objects.create(usuario = request.user, cita= horario, estado_cita = horario.estado) # type: ignore
            print('Listos')
            return redirect('Mis_citas')
        else:
            error = 'No se puede asignar la cita, no esta disponible'
            
    return render(request, 'paginas/horario_citas.html', {'error': error}) # type: ignore


@login_required
def citas_usuario(request):
    print('Entrando a grabar')
    citas = UsuarioCitas.objects.filter(usuario = request.user)
    #formato = [cita_disp.cita for cita_disp in citas] # type: ignore
    return render(request, 'sesiones/citas_usuario.html',{'citas':citas})

@login_required
def cancelar_cita_usuario(request, cita_id):
    try:
        print('Cancelando cita')
        print(cita_id)
        cita_usuario = UsuarioCitas.objects.filter(usuario = request.user, cita = cita_id).first()
        horario = HorarioCita.objects.get(id = cita_id)
        print(horario.fecha)
        print(horario.id) # type: ignore
        accion = request.GET.get('accion')
        
        if accion == 'cancelar':
            cita_usuario = UsuarioCitas.objects.filter(usuario = request.user, cita = cita_id).first()
            horario.estado = 'Disponible'  
            horario.save()
            print(cita_usuario) # type: ignore        
            # cita_usuario.cita.delete()       # type: ignore
            cita_usuario.estado_cita = 'Cancelada' # type: ignore
            cita_usuario.save() # type: ignore
        
        elif accion == 'reprogramar':
            cita_usuario = UsuarioCitas.objects.filter(usuario = request.user, cita = cita_id).first()
            horario.estado = 'Reprogramada'  
            horario.save()
            print(cita_usuario) # type: ignore        
            # cita_usuario.cita.delete()       # type: ignore
            cita_usuario.estado_cita = 'Reprogramada' # type: ignore
            cita_usuario.save() # type: ignore
        
        return redirect('Mis_citas')
        
            
        
    except UsuarioCitas.DoesNotExist:
        raise forms.ValidationError('No tiene permiso para cancelar citas')
    


@login_required
def buscar_citas(request):
    fecha = request.GET.get('fecha')
    medico_id = request.GET.get('id_usuario')
    horario = request.GET.get('hora_cita')

    citas = HorarioCita.objects.all()

    if fecha:
        dato = citas.filter(fecha=fecha)
    if medico_id:
        dato = citas.filter(horario__medico_id=medico_id)
    if horario:
        if horario == 'manana':
            dato = citas.filter(hora__gte='06:00', hora__lte='13:00')
        elif horario == 'tarde':
            dato = citas.filter(hora__gte='13:00', hora__lte='20:00')

    return render(request, 'sesiones/citas_usuario.html', {'citas': dato})

    
    
    
    # bueno quedamos en poder realizar el filtro o busqueda 

#-----------------------------------------------------

# @login_required
# def detalle_tarea(request, tarea_id):
#     if request.method == 'GET':
#         tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
#         print(tarea_id)
#         form = FormularioTarea(instance=tarea)
#         return render(request, 'tarea_detallada.html', {
#             'tarea': tarea,
#             'form': form
#         })
#     else:
#         try:
#             tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
#             print(tarea_id)
#             form = FormularioTarea(request.POST, instance=tarea)
#             form.save()
#             return redirect('loginuser')

#         except ValueError:
#             return render(request, 'tarea_detallada.html', {
#                 'tarea': tarea,
#                 'form': form,
#                 'error': "error al actualizar datos",
#             })


# @login_required  # type: ignore
# def tarea_completada(request, tarea_id):
#     tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
#     print(tarea.title)
#     if request.method == 'POST':
#         tarea.datecompleated = timezone.now()
#         print(tarea.datecompleated)
#         tarea.save()
#         print(tarea.datecompleated)
#         return redirect('loginuser')


# @login_required  # type: ignore
# def tarea_eliminada(request, tarea_id):
#     tarea = get_object_or_404(Task, pk=tarea_id, user=request.user)
#     print(tarea)
#     if request.method == 'POST':
#         print(tarea.title)
#         tarea.delete()
#         return redirect('loginuser')
#     else:
#         print("no se puede enviar datos")

