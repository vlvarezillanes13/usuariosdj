from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import (
    View
)
from django.views.generic.edit import (
    FormView
)
from .forms import (
    LoginForm,
    UpdatePasswordForm, 
    UserRegisterForm,
    VerificacionForm,
)

from .models import User
from .functions import code_generator
# Create your views here.

class UserRegisterView(LoginRequiredMixin,FormView):
    login_url = reverse_lazy('users_app:user-login')
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy("home_app:panel")

    def form_valid(self, form):
        #Generar codigo
        codigo = code_generator()
        #Registrar
        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            nombres = form.cleaned_data['nombres'],
            apellidos = form.cleaned_data['apellidos'],
            genero = form.cleaned_data['genero'],
            codregistro=codigo
        )
        #Enviar Codigo al email
        asunto = 'Confirmarcion de email'
        mensaje = 'Codigo de verificacion: '+ codigo
        email_remitente = 'xovialvarez@gmail.com'
        #
        send_mail(asunto, mensaje, email_remitente, [form.cleaned_data['email'],])
        #Pantalla validacion
        return HttpResponseRedirect(
            reverse('users_app:user-verification',
            kwargs={'pk': usuario.id}
        )
        )

class LoginUser(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home_app:panel")

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse('users_app:user-login')
        )

    
class UpdatePasswordView(LoginRequiredMixin,FormView):
    login_url = reverse_lazy('users_app:user-login')
    template_name = "users/update.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)

class CodeVerificacionView(FormView):
    template_name = "users/verificacion.html"
    form_class = VerificacionForm
    success_url = reverse_lazy('users_app:user-login')
    
    def get_form_kwargs(self):
        kwargs = super(CodeVerificacionView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']
        return kwargs

    def form_valid(self, form):
        #id_user = self.kwargs['pk']
        User.objects.filter(
            id = self.kwargs['pk']
        ).update(
            is_active = True
        )
        return super(CodeVerificacionView, self).form_valid(form)