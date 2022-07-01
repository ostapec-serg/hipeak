from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib.auth import views as auth_views
from django.contrib import messages

from registration_authorisation.models import User
from my_profile.form import ChangingUserPasswordForm, EditUserForm, EditProfileForm
from my_profile.models import Profile


class UpdateUserDataView(UpdateView):
    """
    The class is used to update user data and view profile-related information.
    """
    template_name = 'my_profile/my_profile_page.html'
    form_class = EditProfileForm
    second_form_class = EditUserForm
    extra_context = {'title': 'My profile'}

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        if self.request.user.is_authenticated:
            user_slug = kwargs['slug']
            if self.request.user.profile.slug == user_slug:
                return super().get(request, *args, **kwargs)
            return redirect('main')
        return redirect('authorisation_page')

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        # determine which form is being submitted
        # uses the name of the form's submit button
        if 'form' in request.POST:
            # get the primary form
            form_class = self.get_form_class()
            form_name = 'form'
        else:
            # get the secondary form
            form_class = self.second_form_class
            form_name = 'form2'
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})

    def get_object(self, queryset=None):
        """
        Return the object the view is displaying.
        Subclasses can override this to return any object.
        """
        return get_object_or_404(Profile, slug=self.kwargs['slug'])

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        if 'form2' in self.request.POST:
            if form.cleaned_data['email']:
                self.save_user_data(form)
            return HttpResponseRedirect(self.get_success_url())
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, **kwargs):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(**kwargs))

    def save_user_data(self, form):
        """Save the User model only."""
        user = User.objects.all().get(id=self.object.user_id)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()
        return user

    def get_context_data(self, **kwargs):
        """Insert the forms into the context dict."""
        context = super(UpdateUserDataView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        return context

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return Profile.get_absolute_url(self.object)


class ChangingUserPasswordView(auth_views.PasswordChangeView):
    form_class = ChangingUserPasswordForm
    success_url = 'password_done'
    template_name = 'my_profile/profile_password_settings.html'
    extra_context = {'title': 'Changing password'}

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return reverse_lazy(self.success_url)


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'my_profile/password_reset.html'
    email_list = User.objects.values_list('email', flat=True)
    extra_context = {'title': 'Reset password'}

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        form = self.get_form()
        if form.is_valid():
            user_email = self.request.POST['email']
            if user_email in self.email_list:
                return self.form_valid(form)
            messages.error(self.request, f"{user_email} не зареестрований на сайті")
            return self.form_invalid(form)
        messages.error(self.request, 'Помилка відправки!')
        return self.form_invalid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'my_profile/password_reset_done.html'
    extra_context = {'title': 'Reset Done'}


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'my_profile/password_reset_confirm.html'
    extra_context = {'title': 'Reset Confirm'}


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'my_profile/password_reset_complete.html'
    extra_context = {'title': 'Reset Complete'}


@login_required(login_url='/login')
def password_change_done(request):
    """Logout user after changing password"""
    user = get_object_or_404(User, id=request.user.id)
    if request.user == user:
        logout(request)
        messages.success(request, 'Пароль змінено! Авторизуйтесь!')
        return redirect('authorisation_page')
    return redirect('main')


# re-write
@login_required(login_url='/login')
def profile_delete(request):
    """Delete user profile with user"""
    user = get_object_or_404(User, id=request.user.id)
    if request.user == user:
        # user.is_active = False
        user.delete()
        logout(request)
        return redirect("registration")
    else:
        return redirect("main")
