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
    # Dentro de esta función se encentran dos funciones que vienen de la tabla del listado de usuarios, accionadas por dos botones utilizando la acción de los mismos reutilizando código
    
    # Aquí se trae el parámetro del usuario visto en la tabla con el cual se quiere manipular o accionar     
    perfil = get_object_or_404(CreacionUser, pk=pk)
    admin = request.user # verificar q usuario esta interactuando  
    # variable para obtner un resultado
    habil = perfil.is_active 
    # Condicional            
    if habil == True:
        habil = 'Habilitado'
    else:
        habil = 'Deshabilitado'

    # variable para que se verifique q acción se esta enviando desde el formulario
    accion = request.GET.get('accion')     
    # Condicional según el botón y la acción registrada "?accion=ver"
    # "{% url 'Perfil_Usuario' b1.id %}?accion=habilitar"   
    if accion == 'ver':    
        print(f'Viendo el perfil de {perfil.nombre_completo}')
        # formulario de tratamiento de los datos, la instancia son los datos del usuario
        form = PerfilUsuario(instance=perfil)             
        data = {
            'admin': admin,
            'perfil': perfil,
            'titulo':'Perfil',
            'form': form, 
            'estado':habil        
        }
        return render(request, 'paginas/mi_perfil.html', data)
    # Segunda acción con el botón
    elif accion == 'habilitar':  
        # Nueva condicional      
        if request.method == 'GET':        
            form = FormatoHabilitarUser(instance=perfil)              
            data = {
                'admin': admin,
                'perfil': perfil,
                'form': form,
                'habilitado' : habil
            }
            return render(request, 'sesiones/habilitarUser.html', data)
        
        else:
            # acción cuando se quiere pasar los datos del formulario
            print('Estamos en POST')            
            cuenta = FormatoHabilitarUser(request.POST)
            print(cuenta.data)

            # validación del formulario 
            if cuenta.is_valid():
                # Esto se hace cuando se quiere agregar datos manualmente
                motivo = cuenta.save(commit=False) # Punto de espera
                motivo.id_usuario = perfil
                
                # Mini función para otro modelo
                print(f'Estado {perfil.is_active}')
                if perfil.is_active == True :
                    perfil.is_active = False 
                    estado = 'Deshabilitando'  
                else:
                    perfil.is_active = True 
                    estado = 'Habilitando'
                # Graba en una tabla       
                perfil.save()
                print('Cambio listo')   
                motivo.estado = estado 
                motivo.save() # Graba en la otr tabla 
                print(f'Motivo listo {motivo}')
                # Disecciona después de la función
                return redirect(reverse('Lista_cuentas')) 
            else:
                
                print(f'la cuenta es {cuenta.errors}')
    # Fin y renderiza una pagina al final de todo  
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
   
    
@login_required
def horarioCitas(request):
    # Creación de horario para medicos
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
    # Lista los horarios de los medicos 
    medico = request.GET.get('medico')
    id_medico = CreacionUser.objects.filter(tipo_usuario = 'Medico') # type: ignore
    horario = CrearHorario.objects.all()
    if medico:
        horario = CrearHorario.objects.filter(id_usuario = medico)
    
    data = {
        'titulo':'Listado de cuentas',
        'horarioMed': horario,
        'medicos': id_medico,
    }
    return render(request, 'sesiones/listar_horarios.html', data)
    
@login_required # type: ignore
def editar_horario_medicos(request, pk):
    # Edita el horario creado y almacenado en la base de datos 
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
    # Esta sin funcionamiento hasta el moemnto
    hoy = date.today()  
    medicos = CrearHorario.objects.all()
    # Filtros para la vista mayor que __gt menor q __lt mayor igual q  __gte menoir igual q __lte el dia de hoy
    intervalos = HorarioCita.objects.filter(fecha__gte = hoy).order_by('fecha') # type: ignore
        
    return render(request, 'paginas/horario_citas.html', {'tabla':intervalos, 'medico': medicos})
    
# Tomar cita por el usuario y el administrador
@login_required # type: ignore
def asignar_cita(request):
    print('Ingresando asignación')    
    if request.method == 'POST':
        print('estamos validando')
        id_horario = request.POST.get('cita_horario') # type: ignore
        id_usuario = request.POST.get('usuario_id') # type: ignore
        if id_usuario:
            usuario =  get_object_or_404(CreacionUser, id= id_usuario)
            print(f'Usuario seleccionado {usuario.nombre_completo}')
        else:
            usuario = request.user # Sirve para tomar el id loqueado
        
        horario = HorarioCita.objects.get(id = id_horario)
        if horario.estado == 'Disponible':            
            print(horario.fecha)
            print(horario.id) # type: ignore
            horario.estado = 'Agendada' # type: ignore
            horario.save()
            UsuarioCitas.objects.create(usuario = usuario, cita= horario)
            #cita_disponible = UsuarioCitas.objects.create(usuario = request.user, cita= horario, estado_cita = horario.estado) # type: ignore
            print('Listos')
            
            
            if not id_usuario or int(id_usuario) == request.user.id:
                messages.success(request, f'Cita asignada correctamente')
                return redirect('Mis_citas')
            else:
                messages.success(request, f'Cita asignada correctamente a {usuario.nombre_completo} ')
                print(f'Se envió satisfactoriamente el usuario {usuario.nombre_completo}')
                return redirect('Citas_programadas')
                
                # # Enviar correo al usuario que ha tomado la cita
                # send_mail(
                #     'Cita Agendada',
                #     f'Hola {usuario.nombre_completo}, su cita ha sido agendada para el {horario.fecha} a las {horario.hora_cita}.',
                #     settings.EMAIL_HOST_USER,
                #     [usuario.email],
                #     fail_silently=False,
                # )
            
        else:            
            error = 'No se puede asignar la cita, no esta disponible'
            messages.error(request, error)
            return render(request, 'paginas/horario_citas.html', {'error': error}) # type: ignore
    return render(request, 'paginas/horario_citas.html') # type: ignore

@login_required
def citas_usuario(request):
    print('Entrando a mis citas')
    citas = UsuarioCitas.objects.filter(usuario = request.user)
    #formato = [cita_disp.cita for cita_disp in citas] # type: ignore
    return render(request, 'sesiones/citas_usuario.html',{'citas':citas})

@login_required # type: ignore
def citas_medico(request):
    print('Entrando a citas por medico medicos')
    # Se filtran las citas por el usuario que esta logueado
    medico = CreacionUser.objects.get(username =request.user) # type: ignore
    print(f'El medico es {medico.pk}')
    citas = UsuarioCitas.objects.filter(cita__horario__id_usuario= medico.pk).order_by('cita__fecha') # type: ignore
    #formato = [cita_disp.cita for cita_disp in citas] # type: ignore
    return render(request, 'sesiones/citas_medico.html',{'citas':citas})



@login_required # type: ignore
def citas_programadas(request):
    print('Entrando a citas programadas')
    estado = request.POST.get('estado')
    citas = UsuarioCitas.objects.all().order_by('cita__fecha')
    if estado:
        citas = citas.filter(cita__estado=estado).order_by('cita__fecha')
    return render(request, 'paginas/citas_programadas.html',{'citas':citas})

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

# Buscar citas enlistados 
@login_required # type: ignore
def buscar_citas(request):   
    usuario_id = request.GET.get('usuario_id') or request.POST.get('usuario_id') # type: ignore
    print(f'pasando el usuario {usuario_id}')
    citas = None  
    titu = 'Esperando resultados'  
    hoy = date.today()           
    if request.method == 'POST':
        datos = BarraBusquedaCitas(request.POST)
        if datos.is_valid():
            print('Entrando a buscar')
            fecha_inicio = datos.cleaned_data['fecha_inicio']
            fecha_final = datos.cleaned_data['fecha_final']
            medico = datos.cleaned_data['medico'] 
            hora = datos.cleaned_data['hora']            
            # citas =HorarioCita.objects.filter(fecha__gte = hoy).order_by('fecha') 
            # citas = HorarioCita.objects.all()       
            citas = HorarioCita.objects.all().order_by('fecha')      
            if fecha_inicio:
                citas = citas.filter(fecha__gte = fecha_inicio)
            if fecha_final:
                citas = citas.filter(fecha__lte = fecha_final)
            if medico:
                # Aqui se marca una instancia de modelos al cual apuntan
                citas = citas.filter(horario__id_usuario= medico )               
            if hora == 'manana':
                citas = citas.filter(hora_cita__gte='06:00', hora_cita__lte='12:00')
            elif hora == 'tarde':
                citas = citas.filter(hora_cita__gte='12:00', hora_cita__lte='20:00')    
           
            print('Procesandos')
        else:
            print('Problemas de validación del form')  
    
    else:
        print('Ingresando primeo')
        datos = BarraBusquedaCitas()
        
        
    return render(request,'paginas/horario_citas.html', {'formato': datos, 'datos':citas ,'titulo': titu, 'usuario_id':usuario_id})
        
            
# Búsqueda de usuarios 
@login_required
def busquedaUser(request):
    form = BusquedaUsuario()
    usuario = None
    if request.method == 'POST':
        form = BusquedaUsuario(request.POST)
        if form.is_valid():
            numero = form.cleaned_data['identificacion']
            tipo = form.cleaned_data['tipo_id']
            print(numero, tipo)
            usuario = CreacionUser.objects.filter(numero_id = numero, tipo_id = tipo)
    
    return render(request, 'sesiones/busqueda_usuario.html', {'form':form, 'dato':usuario})

# Búsqueda de asistencia de citas por usuario para el registro
@login_required
def busqueda_AsitenciaUser(request):
    form = BusquedaUsuario()
    citas = UsuarioCitas.objects.all().order_by('cita')    
    cita_id = None
    usuario = None
    if request.method == 'POST':
        if 'buscar_usuario' in request.POST:
            print('Entrando a buscar usuario')        
            form = BusquedaUsuario(request.POST)
            if form.is_valid():
                numero = form.cleaned_data['identificacion']
                tipo = form.cleaned_data['tipo_id']
                print(numero, tipo)
                usuario = UsuarioCitas.objects.filter(usuario__numero_id = numero, usuario__tipo_id = tipo)
                print(usuario.values('usuario__pk')) # type: ignore
            return render(request, 'sesiones/asistencia_citas.html', {'form':form, 'datos':usuario})
            
        elif 'cita_asistencia' in request.POST:
            print('Entrando a buscar cita')
            cita_id = request.POST.get('cita_asistencia')
            print(f'Buscando la cita {cita_id}')
            uno = UsuarioCitas.objects.get(pk = cita_id)
            print(f'citas encontradas {uno.cita.asistencia}') # type: ignore
            if uno.cita.asistencia == True:
                # uno.cita.asistencia = False
                uno.cita.save() 
            else:
                # uno.cita.asistencia = True
                uno.cita.save()
            print(f'cita actualizada {uno.cita.asistencia}') # type: ignore         
    
    return render(request, 'sesiones/asistencia_citas.html', {'form':form, 'citas':citas})


# listado de asiastencia de citas
@login_required # type: ignore
def asistencia_citas(request):
    asistencia = UsuarioCitas.objects.filter(cita__asistencia = "Asistio").order_by('cita__fecha')
    
    return render(request, 'sesiones/lista_asistencia.html', {'datos':asistencia})


@login_required  # type: ignore
def registrar_historia_clinica(request):
    medico = request.user
    form = FormularioHistoriaClinica()
    
    if request.method == 'POST':
        num = request.POST.get('buscar_paciente')  # type: ignore
        grabar = request.POST.get('guardar_historia')  # type: ignore
        print('Entrando a registrar historia clinica')
        
        if 'buscar_paciente' in request.POST:
        # Se obtiene el numero de id del paciente a buscar    
            print(f'Buscando paciente con numero de id: {num}')
            paciente = CreacionUser.objects.filter(numero_id=num).first()  # type: ignore
            id_cita = UsuarioCitas.objects.filter(usuario = paciente).first()  # type: ignore
            if paciente:
                print(f'El paciente es {paciente} y la cita es {id_cita.cita} del medico {id_cita.cita.horario.id_usuario.nombre_completo}') # type: ignore
               # Si se encuentra el paciente, se obtienen sus citas y se renderiza el formulario    
            else: 
                print('Paciente no encontrado')
            if paciente: # type: ignore
                print(f'Paciente encontrado: {paciente.nombre_completo}')
                citas = UsuarioCitas.objects.filter(usuario__username = paciente).order_by('cita__fecha')
                consulta = HistoriaClinica.objects.filter(id_cita__usuario = paciente).order_by('id_cita__cita__fecha') # type: ignore
                print(f'Historias clinicas del paciente encontrado: {consulta}')
                print(f'Citas del paciente encontrado: {citas}')
                form = FormularioHistoriaClinica(id_cita = paciente) # type: ignore
                return render(request, 'sesiones/historia_clinica.html', {'form': form, 'paciente': paciente, 'citas': citas, 'consulta': consulta})   
            # else:        
            #     print('Paciente no encontrado')
    
            #     return render(request, 'sesiones/historia_clinica.html', {'form': form})

                
    
        elif 'guardar_historia' in request.POST:            
            print('Guardando historia clinica')
            id_cita = request.POST.get('id_cita') # type: ignore
            motivo = request.POST.get('motivo_consulta') # type: ignore
            diagnostico = request.POST.get('diagnostico') # type: ignore
            tratamiento = request.POST.get('tratamiento') # type: ignore
            print(f'ID de cita: {id_cita}, motivo: {motivo}, diagnostico: {diagnostico}, tratamiento: {tratamiento}')
            form = FormularioHistoriaClinica()
            # Validaciones de los campos del formulario
            if not id_cita:
                raise forms.ValidationError('Debe seleccionar una cita para continuar.')
            elif not motivo:
                raise forms.ValidationError('El motivo de consulta es obligatorio.')                
            elif not diagnostico:
                raise forms.ValidationError('El diagnóstico es obligatorio.')   
            elif not tratamiento:
                raise forms.ValidationError('El tratamiento es obligatorio.')   
            elif len(motivo) < 10:   
                raise forms.ValidationError('El motivo de consulta debe tener al menos 10 caracteres.')
            elif len(diagnostico) < 10:   
                raise forms.ValidationError('El diagnóstico debe tener al menos 10 caracteres.')    
            elif len(tratamiento) < 10:   
                raise forms.ValidationError('El tratamiento debe tener al menos 10 caracteres.')    
            
            else:
                # Si el formulario es enviado, se crea una instancia del formulario con los datos del POST
                historia = HistoriaClinica.objects.create(id_cita_id = id_cita, motivo_consulta = motivo, diagnostico = diagnostico, tratamiento = tratamiento) # type: ignore
                historia.save()
                messages.success(request, 'Historia clinica guardada exitosamente')
                return redirect('Historia_Clinica') 
            
            
            
            
            # form = FormularioHistoriaClinica(request.POST, id_cita = id_cita) # type: ignore
            # print(f'ID de cita: {id_cita}')
            
            # print(f'Formulario recibido:') # type: ignore
            # print(form.data.get('id_cita')) # type: ignore
            # print(form.data.get('motivo_consulta')) # type: ignore
            # print(form.data.get('diagnostico')) # type: ignore
            # print(form.data.get('tratamiento')) # type: ignore
            
            # #print(form.id_cita)
            # if form.is_valid():
            #     historia = form.save(commit=False)
            #     print('Historia clinica validada y lista para guardar')
            #     historia.medico = medico  # type: ignore            
            #     historia.id_cita = id_cita  # type: ignore
            #     print("esperando para guardar")
            #     historia.save()
            #     messages.success(request, 'Historia clinica guardada exitosamente')
            #     return redirect('Registrar_historia_clinica') 
            # else:
            #     print('Error al guardar historia clinica')
            #     #messages.error(request, 'Error al guardar historia clinica, por favor verifique los datos')
            #     #return render(request, 'sesiones/historia_clinica.html', {'form': form, 'error': 'Error al guardar historia clinica'})     
    
    
    elif medico:
        form = FormularioHistoriaClinica(initial= {'medico':medico.pk}) # type: ignore



    else:        
        print('Paciente no encontrado')
        
        
    
    
    return render(request, 'sesiones/historia_clinica.html', {'form': form})



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

