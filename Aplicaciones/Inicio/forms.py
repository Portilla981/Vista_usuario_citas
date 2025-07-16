# from typing import Any, Iterable, Sequence
from django import forms
# from django.forms.widgets import _OptAttrs
from .models import *
# from django.forms.widgets import TimeInput, SelectDateWidget, _OptAttrs
from datetime import datetime

class Formato_Contacto(forms.ModelForm):
    
    class Meta:
        model = ContactarUsuario
        # Forma manual de uno por uno 
        #fields = ['nombres', 'apellidos', 'telefono', 'motivo', 'mensaje', 'contactar'] 
        # Forma automática de todos los campos 
        fields = '__all__'
        
class Formato_RegistroU(forms.ModelForm):    
    password1 = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repita la contraseña')
        
    # Clase para mostrar los campos necesarios en el formulario
    class Meta:
        model = CreacionUser
        # Se añaden tanto los campos del User como los creados en el formato adstrato
        fields = ['tipo_id','numero_id','first_name','last_name', 'telefono','email', 'tipo_usuario','is_active','username', 'password1', 'password2']
        
        help_texts ={
            'tipo_id': '',
            'numero_id': '',
            'first_name': '',
            'last_name':'',
            'telefono':'',
            'email':'',
            'tipo_usuario':'',
            'is_active':'',
            'username':'',
            'date_joined': '',
            'last_login':'',
            
        }


    # Primer método sin tomar parámetros dentro del modelo
    def limpiar_password(self):
        dato1 = self.cleaned_data.get('password1') 
        dato2 = self.cleaned_data.get('password2')
        if dato1 and dato2 and dato1 != dato2:
            print('Validación correcta')
            return forms.ValidationError('las contraseñas ingresadas no son iguales')        
        return dato2  
    
    # Función para encriptar contraseña
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
    
        
class Iniciar_Sesion(forms.Form):
    usuario = forms.CharField(max_length=12,  label='Usuario', min_length=8)
    password = forms.CharField(widget=forms.PasswordInput(render_value=True),label='Contraseña',)
    

class PerfilUsuario(forms.ModelForm):    
    
    class Meta:        
        model = CreacionUser
        # Se añaden tanto los campos del User como los creados en el formato adstrato
        fields = ['tipo_id','numero_id','first_name','last_name', 'telefono','email', 'tipo_usuario','username', 'date_joined','last_login']
        
        # forma de quitar la ayuda de texto en los input
        help_texts ={
            'tipo_id': '',
            'numero_id': '',
            'first_name': '',
            'last_name':'',
            'telefono':'',
            'email':'',
            'tipo_usuario':'',
            'is_active':'',
            'username':'',            
            'date_joined': '',
            'last_login':'',           
        }
        
        widgets={
            'tipo_id': forms.TextInput(attrs={'readonly': True}),
            'numero_id': forms.TextInput(attrs={'readonly': True},),
            'first_name': forms.TextInput(attrs={'readonly': True}),
            'last_name':forms.TextInput(attrs={'readonly': True}),
            'telefono':forms.TextInput(attrs={'readonly': True}),
            'email':forms.EmailInput(attrs={'readonly': True}),
            'tipo_usuario':forms.TextInput(attrs={'readonly': True}),
            'is_active':forms.CheckboxInput(attrs={'readonly': True}),
            'username':forms.TextInput(attrs={'readonly': True}),            
            'date_joined': forms.TextInput(attrs={'readonly': True}),
            'last_login':forms.TextInput(attrs={'readonly': True}),            
        }

    
class EditarUsuario(forms.ModelForm):    
    
    class Meta:        
        model = CreacionUser
        # Se añaden tanto los campos del User como los creados en el formato abstrato
        fields = ['tipo_id','numero_id','first_name','last_name', 'telefono','email', 'tipo_usuario','username', 'is_active']
        
        # froma de qquitar la ayuda de texto en los input
        help_texts ={
            'tipo_id': '',
            'numero_id': '',
            'first_name': '',
            'last_name':'',
            'telefono':'',
            'email':'',
            'tipo_usuario':'',
            'is_active':'',
            'username':'',
            'date_joined': '',
            'last_login':'',
        }

class BarraBusqueda(forms.Form):
    buscar = forms.CharField(label='Buscar:', max_length=100)
    

# funcione spara esytablecer el dia y la hora actual para el formato 
'''
class CustomYearSelect(SelectDateWidget):
    def __init__(self, years= None, *args, **kwargs):
        if years is None:
            current_year = datetime.now().year
            years = range(current_year, current_year+11)        
        super().__init__(years=years, *args, **kwargs)
        
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        year_field = context['widget']['subwidgets'] [0]
        context['widget']['subwidgets'][0] = {**year_field, 'choises': [(year, year) for year in self.years]}
        
        return context
            
class CustomTimeInput(TimeInput):
    def __init__(self, attrs= None, format=None):
        attrs= attrs or {}
        attrs.update({'min': '07:00', 'max': '19:00'})
        super().__init__(attrs, format)
        '''

    
class CreacionHorarioCitas(forms.ModelForm):
    
    class Meta:
        model = CrearHorario
        fields = '__all__'           
        widgets = {
            'fecha': forms.DateInput(attrs={'type':'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type':'time'}),
            'hora_final': forms.TimeInput(attrs={'type':'time'}),
        }
        
        # def __init__(self, *args, **kwargs):
        #     print('Buscando medicos')
        #     super(CreacionHorarioCitas, self).__init__(*args, **kwargs) # type: ignore
        #     self.fields['id_usuario_id'].queryset = CreacionUser.objects.filter(tipo_usuario = 'Medico') # type: ignore
        #     # self.fields['id_medico'].label_from_instance = lambda obj: "%s %s" % (obj.first_name, obj.last_name)      #f'{obj.first_name} {obj.last_name}' # type: ignore
            
    