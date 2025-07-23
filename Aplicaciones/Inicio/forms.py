
from django import forms
# from django.db.models.base import Model
from .models import *
from datetime import date, datetime, time
from django.utils import timezone
# import re
# from django.forms import ModelChoiceField

class Formato_Contacto(forms.ModelForm):

    class Meta:
        model = ContactarUsuario
        # Forma manual de uno por uno
        # fields = ['nombres', 'apellidos', 'telefono', 'motivo', 'mensaje', 'contactar']
        # Forma automática de todos los campos
        fields = '__all__'


class Formato_RegistroU(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password2 = forms.CharField(
        widget=forms.PasswordInput, label='Repita la contraseña')

    # Clase para mostrar los campos necesarios en el formulario
    class Meta:
        model = CreacionUser
        # Se añaden tanto los campos del User como los creados en el formato adstrato
        fields = ['tipo_id', 'numero_id', 'first_name', 'last_name', 'telefono','email', 'tipo_usuario', 'is_active', 'username', 'password1', 'password2']

        help_texts = {
            'tipo_id': '',
            'numero_id': '',
            'first_name': '',
            'last_name': '',
            'telefono': '',
            'email': '',
            'tipo_usuario': '',
            'is_active': '',
            'username': '',
            'date_joined': '',
            'last_login': '',

        }

    # Método sin tomar parámetros dentro del modelo para la validaciones 
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            print('Validación correcta')
            raise forms.ValidationError('las contraseñas ingresadas no son iguales')
        return password2
    
    def clean_first_name(self):
        nombre = self.cleaned_data.get('first_name')
        if not re.match(r'^[a-zA-Z]+$', nombre.strip()): # type: ignore
            raise forms.ValidationError('El nombre solo puede recibir letras')
        return nombre.strip() # type: ignore
    
    def clean_last_name(self):
        apellido = self.cleaned_data.get('last_name')
        if not re.match(r'^[a-zA-Z]+$', apellido.strip()):  # type: ignore
            raise forms.ValidationError('El apellido solo puede recibir letras')
        return apellido.strip() # type: ignore
    

    # Función para encriptar contraseña
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class Iniciar_Sesion(forms.Form):
    usuario = forms.CharField(max_length=12,  label='Usuario', min_length=8)
    password = forms.CharField(widget=forms.PasswordInput(
        render_value=True), label='Contraseña',)


class PerfilUsuario(forms.ModelForm):

    class Meta:
        model = CreacionUser
        # Se añaden tanto los campos del User como los creados en el formato adstrato
        fields = ['tipo_id', 'numero_id', 'first_name', 'last_name', 'telefono','email', 'tipo_usuario', 'username', 'date_joined', 'last_login']

        # forma de quitar la ayuda de texto en los input
        help_texts = {
            'tipo_id': '',
            'numero_id': '',
            'first_name': '',
            'last_name': '',
            'telefono': '',
            'email': '',
            'tipo_usuario': '',
            'is_active': '',
            'username': '',
            'date_joined': '',
            'last_login': '',
        }

        widgets = {
            'tipo_id': forms.TextInput(attrs={'readonly': True}),
            'numero_id': forms.TextInput(attrs={'readonly': True},),
            'first_name': forms.TextInput(attrs={'readonly': True}),
            'last_name': forms.TextInput(attrs={'readonly': True}),
            'telefono': forms.TextInput(attrs={'readonly': True}),
            'email': forms.EmailInput(attrs={'readonly': True}),
            'tipo_usuario': forms.TextInput(attrs={'readonly': True}),
            'is_active': forms.CheckboxInput(attrs={'readonly': True}),
            'username': forms.TextInput(attrs={'readonly': True}),
            'date_joined': forms.TextInput(attrs={'readonly': True}),
            'last_login': forms.TextInput(attrs={'readonly': True}),
        }


class EditarUsuario(forms.ModelForm):

    class Meta:
        model = CreacionUser
        # Se añaden tanto los campos del User como los creados en el formato abstrato
        fields = ['tipo_id', 'numero_id', 'first_name', 'last_name',
                  'telefono', 'email', 'tipo_usuario', 'username', 'is_active']

        # froma de qquitar la ayuda de texto en los input
        help_texts = {
            'tipo_id': '',
            'numero_id': '',
            'first_name': '',
            'last_name': '',
            'telefono': '',
            'email': '',
            'tipo_usuario': '',
            'is_active': '',
            'username': '',
            'date_joined': '',
            'last_login': '',
        }


class BarraBusqueda(forms.Form):
    buscar = forms.CharField(label='Buscar:', max_length=100)

# Se crea la clase para personalizar el campo de id_usuario
class UsuarioModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):        
        return obj.nombre_completo # type: ignore

class CreacionHorarioCitas(forms.ModelForm):
    # id_usuario = UsuarioModelChoiceField(queryset=CreacionUser.objects.filter(tipo_usuario = 'Medico'), label= 'Medico', empty_label= 'Seleccione el medico')
    # Se llama al modelo creado por la función por ser personalizada
    id_usuario = UsuarioModelChoiceField(queryset=CreacionUser.objects.none(), label= 'Medico', required=False)
    
    # Función para crear una variable de comparación y de acción dentro tanto del formulario como de la validación del mismo
    def __init__(self, *args, **kwargs):
        usuario_actual = kwargs.pop('usuario_actual',None)
        super().__init__(*args, **kwargs)
        
        # Condicional como acción de la lógica
        if usuario_actual:
            if usuario_actual.is_superuser:
                self.fields['id_usuario'].queryset = CreacionUser.objects.filter(tipo_usuario = 'Medico') # type: ignore
                self.fields['id_usuario'].empty_label = 'Seleccione el medico' # type: ignore
            else:
                self.fields['id_usuario'].queryset = CreacionUser.objects.filter(pk= usuario_actual.id) # type: ignore
                self.fields['id_usuario'].initial = usuario_actual.id
                self.fields['id_usuario'].widget.attrs['readonly']= True
        
    
    class Meta:
        model = CrearHorario
        fields = '__all__'
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'min': '06:00', 'max': '18:00'}),
            'hora_final': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'min': '06:00', 'max': '18:00'}),
        }

    def clean(self):
        print('Ingreso a validar')
        cleaned_data = super().clean()
        usuario = self.cleaned_data.get('id_usuario')
        print(usuario)
        fecha_1 = self.cleaned_data.get('fecha') 
        print(fecha_1)
        hora_1 = self.cleaned_data.get('hora_inicio') 
        fecha_actual = date.today()
        ahora = datetime.now()
        fecha_hora = datetime.combine(fecha_1, hora_1) # type: ignore        
        hora_2 = self.cleaned_data.get('hora_final')         
        inicio = time(6,0)
        final = time(19,0)
        hora_espera = time(17,0)
        espera = timedelta(hours= 2) # type: ignore
        hora_espera = ahora + espera 
        hora_aceptada = datetime.combine(date.today(), hora_1 )+ espera        # type: ignore
        
        
        if fecha_1.weekday() >= 6: # type: ignore
            raise forms.ValidationError('La fecha debe ser entre lunes y viernes.')
        
        elif fecha_hora < ahora:
            raise forms.ValidationError('La fecha o la hora no son correctos.')
        
        elif hora_1 > hora_2: # type: ignore
            raise forms.ValidationError('La hora de inicio es mayor a la hora final.')
            
        elif hora_1 < inicio or hora_1 > final: # type: ignore
            raise forms.ValidationError('La hora de inicio es incorrecta debe ser entre las 06:00 y 19:00 horas.')
        
        elif hora_2 < inicio or hora_2 > final: # type: ignore
            raise forms.ValidationError('La hora de final es incorrecta debe ser entre las 06:00 y 19:00 horas.')
        
        elif fecha_1 == timezone.now() and hora_aceptada < hora_espera and hora_aceptada >= final: # type: ignore
            raise forms.ValidationError('La disponibilidad de la hora de inicio es dos horas después de la hora actual asi como dos horas antes de las 18:00, esto por cuestiones de facilidad y plasticidad.')
        
        print('paso todo')

class Formato_editar_horario(forms.ModelForm):
    #id_usuario = forms.CharField(label= 'Medico', initial= 'medico', disabled=True)
    
    class Meta:
        model = CrearHorario
        fields = ['fecha', 'hora_inicio', 'hora_final']
        widgets = {
            # 'id_usuario': forms.TextInput(attrs= {'readonly': True, 'value':'{{medico.nombre_completo}}' }),
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'min': '06:00', 'max': '18:00'}),
            'hora_final': forms.TimeInput(format='%H:%M', attrs={'type': 'time', 'min': '06:00', 'max': '18:00'}),
        }
    
    def clean(self):
        print('Ingreso a validar edición de datos')
        cleaned_data = super().clean()
        # usuario = self.cleaned_data.get('id_usuario')
        # print(usuario)
        fecha_1 = self.cleaned_data.get('fecha') 
        print(fecha_1)
        hora_1 = self.cleaned_data.get('hora_inicio') 
        fecha_actual = date.today()
        ahora = datetime.now()
        fecha_hora = datetime.combine(fecha_1, hora_1) # type: ignore        
        hora_2 = self.cleaned_data.get('hora_final')         
        inicio = time(6,0)
        final = time(19,0)
        hora_espera = time(17,0)
        espera = timedelta(hours= 2) # type: ignore
        hora_espera = ahora + espera 
        hora_aceptada = datetime.combine(date.today(), hora_1 )+ espera        # type: ignore
        
        
        if fecha_1.weekday() >= 6: # type: ignore
            raise forms.ValidationError('La fecha debe ser entre lunes y viernes.')
        
        elif fecha_hora < ahora:
            raise forms.ValidationError('La fecha o la hora no son correctos.')
        
        elif hora_1 > hora_2: # type: ignore
            raise forms.ValidationError('La hora de inicio es mayor a la hora final.')
            
        elif hora_1 < inicio or hora_1 > final: # type: ignore
            raise forms.ValidationError('La hora de inicio es incorrecta debe ser entre las 06:00 y 19:00 horas.')
        
        elif hora_2 < inicio or hora_2 > final: # type: ignore
            raise forms.ValidationError('La hora de final es incorrecta debe ser entre las 06:00 y 19:00 horas.')
        
        elif fecha_1 == timezone.now() and hora_aceptada < hora_espera and hora_aceptada >= final: # type: ignore
            raise forms.ValidationError('La disponibilidad de la hora de inicio es dos horas después de la hora actual asi como dos horas antes de las 18:00, esto por cuestiones de facilidad y plasticidad.')
        
        print('paso todo')

        