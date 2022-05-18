from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from registration_authorisation.form import RegistrationForm, LoginForm


class Registration(CreateView):
    form_class = RegistrationForm
    template_name = 'registration_authorisation/registration.html'
    success_url = '/login'


class Authorisation(LoginView):
    form_class = LoginForm
    template_name = 'registration_authorisation/login.html'
    success_url = ''
