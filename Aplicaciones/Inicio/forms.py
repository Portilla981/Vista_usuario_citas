from django import forms
from .models import *

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
        # Se añaden tanto los campos del User como los creados en el formato abstrato
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
            #'password':forms.TextInput(attrs={'readonly': True}),
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
        # Se añaden tanto los campos del User como los creados en el formato abstrato
        fields = ['tipo_id','numero_id','first_name','last_name', 'telefono','email', 'tipo_usuario','username', 'is_active', 'date_joined','last_login']
        
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
            #'password':forms.TextInput(attrs={'readonly': True}),
            'date_joined': '',
            'last_login':'',
            #'fecha_actualizacion':'',
            
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
            #'password':forms.TextInput(attrs={'readonly': True}),
            'date_joined': forms.TextInput(attrs={'readonly': True}),
            'last_login':forms.TextInput(attrs={'readonly': True}),
            #'fecha_actualizacion':forms.TextInput(attrs={'readonly': True}),
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
            #'password':forms.TextInput(attrs={'readonly': True}),
            'date_joined': '',
            'last_login':'',
            #'fecha_actualizacion':'',            
        }

class BarraBusqueda(forms.Form):
    buscar = forms.CharField(label='Buscar:', max_length=100)
    