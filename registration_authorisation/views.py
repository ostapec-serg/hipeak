import threading
from string import ascii_lowercase
from random import choices

from django.contrib.auth.views import LoginView
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib import messages

from registration_authorisation.form import RegistrationForm, LoginForm
from registration_authorisation.models import User


class Authorisation(LoginView):
    """Authorisation class"""
    form_class = LoginForm
    template_name = 'registration_authorisation/login.html'
    success_url = ''
    redirect_authenticated_user = True


class Registration(CreateView):
    """Registration class with email confirmation """
    form_class = RegistrationForm
    template_name = 'registration_authorisation/registration.html'
    success_url = '/registration'
    session_expiry_period = 172800

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        if self.request.user.is_authenticated:
            return redirect('main')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: if user don't exist,
        instantiate a form instance with the passed
        POST variables and then check if it's valid.
        if user exist but not activate and 'last_login' is None,
        send new confirmation email
        """
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)
        if email and username:
            check_user = self.check_user(email)
            if check_user:
                self.object = check_user
                if self.check_password():
                    self.object.username = username
                    self.object.save()
                    code = self.get_random_code()
                    self.send_code(username, code)
                    messages.success(
                        self.request,
                        "Для підтвердження реєстрації ми "
                        "відправили лист на вказану пошту!"
                    )
                    return redirect('login')
        self.object = None
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        username = form.cleaned_data["username"]
        code = self.get_random_code()
        self.object = form.save(commit=True)
        self.object.is_active = False
        self.object.save()
        self.send_code(username, code)
        message = messages.success(
            self.request,
            "Для підтвердження реєстрації ми "
            "відправили лист на вказану пошту!"
        )
        self.extra_context = {'message': message}
        return super().form_valid(form)

    def send_code(self, username, code):
        """
        Preparing session data and save it.
        Build verification code and start
        'sending email thread'
        """
        self.request.session.set_expiry(self.session_expiry_period)
        self.request.session["code"] = code
        self.request.session["username"] = username
        self.request.session.save()
        session_id = self.request.session.session_key
        code = code + session_id
        trd_send_registration_code = self.create_tread(code)
        trd_send_registration_code.start()

    def create_tread(self, code):
        """Creating thread for sending mail"""
        trd_send_registration_code = threading.Thread(
            target=self.sending_verification_code,
            args=(code,),
            name='send_registration_code'
        )
        return trd_send_registration_code

    def check_user(self, email):
        """Checking if user exist"""
        try:
            user = User.objects.get(email=email)
            if user and user.is_active is False:
                if not user.last_login:
                    return user
        except User.DoesNotExist:
            return None

    def sending_verification_code(self, code):
        """Sending mail with activation url to user"""
        message = self.build_message(code, self.request)
        self.object.email_user(message['subject'], message['message'])

    @staticmethod
    def get_random_code():
        """Generate random security code"""
        code = ''.join(choices(ascii_lowercase, k=12))
        return code

    def build_message(self, code, request):
        """Build message for email"""
        url = self.get_email_url(code, request)
        subject = "Registration on hipeak.portal"
        message = f"Ви отримали цього листа тому, що Вашу почтову одресу " \
                  f"вказано для реєстрації на порталі hipeak.portal як {self.object.username}.\n" \
                  f"Якщо це були не Ви, проігноруйте цей лист!\n" \
                  f"Для підтвердження реєстрації перейдіть за посиланням\n" \
                  f"{url} \n" \
                  f"!Посилання дійсне 2 дні!"
        if subject and message:
            message = {
                'message': message,
                'subject': subject
            }
            return message

    @staticmethod
    def get_email_url(code, request):
        """Generate url for user confirmation"""
        from django.contrib.sites.shortcuts import get_current_site
        current_site = get_current_site(request)
        name = current_site.name
        domain = current_site.domain
        url = f"https://{domain}{reverse_lazy('registration_confirm', kwargs={'slug': code})}"
        return url

#  IN PROGRESS
    # def check_password(self, *args, **kwargs):
    #     """checking not activated user password"""
    #     pword1 = self.request.POST.get("password1", None)
    #     pword2 = self.request.POST.get("password2", None)
    #     if pword1 and pword2 and (pword1 == pword2):
    #         # self.object.password = pword2
    #         # self.object.save()
    #         return True
    #     self.object = None
    #     return super().post(self.request, *args, **kwargs)
#  IN PROGRESS


class EmailRegisterView(TemplateView):
    request_code = None
    success_url = "/login"

    def get(self, request, *args, **kwargs):
        """
        Render a template. Pass keyword arguments
        from the URLconf to the context.
        """
        if 'slug' in kwargs:
            self.request_code = kwargs['slug']  # works fine
            if len(self.request_code) == 44:
                checking = self.checking_session_code()
                if checking:
                    self.save()
                    self.clean_session()
                    messages.success(
                        self.request,
                        "Реєстрація підтверджена. Авторизуйтесь!"
                    )
                    return redirect('login')
        messages.error(self.request, "Посилання не дійсне!")
        return redirect('login')

    def checking_session_code(self):
        """Compares 'code_session' and 'request_code'"""
        session_data = self.get_session_data()
        if session_data:
            code_session = self.request_code[:12]
            session_code = session_data['code']
            if code_session == session_code:
                return True
            messages.error(self.request, "Не вірний код!")
            return redirect('login')

    def save(self):
        """Activates user"""
        user = self.get_user_from_session()
        user.is_active = True
        return user.save()

    def get_user_from_session(self):
        """ Get session user. Return user if exist"""
        session_obj_data = self.get_session_data()
        try:
            username = session_obj_data['username']
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            messages.error(self.request, "Користувач не зареєстрований!")
            return redirect('registration')

    def get_session_data(self):
        """Return decoded session data"""
        user_session_key = self.request_code[12:]
        try:
            session_obj = Session.objects.get(pk=user_session_key)
            session_obj_data = session_obj.get_decoded()
            return session_obj_data
        except Session.DoesNotExist:
            return None

    def clean_session(self):
        """Clean session"""
        user_session_key = self.request_code[12:]
        session_obj = Session.objects.filter(session_key=user_session_key)
        session_obj.delete()
