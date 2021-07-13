from django import forms
from django.contrib.auth import authenticate
from django.db import models

from .models import User

class UserRegisterForm(forms.ModelForm):
    
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña'
            }
        )
    )
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Repetir Contraseña'
            }
        )
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
        )

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Username',
                'style':'{ margin: 10px }'
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña'
            }
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username_ = self.cleaned_data['username']
        password_ = self.cleaned_data['password']
        
        if not authenticate(username=username_, password=password_):
            raise forms.ValidationError('Los datos del usuario no son correctos')
        
        return self.cleaned_data

class UpdatePasswordForm(forms.Form):
      
    password1 = forms.CharField(
        label='Contraseña Actual',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña Nueva',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder':'Contraseña Nueva'
            }
        )
    )
    def __init__(self, *args, **kwargs):

        self.request = kwargs.pop('request')
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()
        username_ = self.request.user.username
        password_ = self.cleaned_data['password1']
        
        if not authenticate(username=username_, password=password_):
            raise forms.ValidationError('Contraseña Actual Incorrecta')

        return self.cleaned_data

class VerificacionForm(forms.Form):
    codregistro = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):

        self.id_user = kwargs.pop('pk')
        super(VerificacionForm, self).__init__(*args, **kwargs)

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('el código es incorrecto')
        else:
            raise forms.ValidationError('el código es incorrecto')
