from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import UpdateView

from my_profile.form import ChangingUserPasswordForm, EditUserForm, EditProfileForm
from my_profile.models import Profile


class UpdateUserDataView(UpdateView):
    template_name = 'my_profile/my_profile_page.html'
    form_class = EditUserForm
    second_form_class = EditProfileForm

    def get_context_data(self, **kwargs):
        context = super(UpdateUserDataView, self).get_context_data(**kwargs)
        context['profile_data'] = User.objects.prefetch_related().get(id=self.request.user.id)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.POST)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.POST)
        return context

    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        # get the user instance
        self.object = self.get_object()
        # determine which form is being submitted
        # uses the name of the form's submit button
        if 'form' in request.POST:
            # get the primary form
            form_class = self.get_form_class()
            form_name = 'form'
            # get the secondary form
        else:
            form_class = self.second_form_class
            form_name = 'form2'
        # get the form
        form = self.get_form(form_class)
        # validate
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(**{form_name: form})

    def get_queryset(self):
        """
        Return the `QuerySet` that will be used to look up the object.
        This method is called by the default implementation of get_object() and
        may not be called if get_object() is overridden.
        """
        if 'form' in self.request.POST:
            return User.objects.select_related('profile')
        else:
            return Profile.objects.all().select_related('user')

    def get_success_url(self):
        """Return the URL to redirect to after processing a valid form."""
        return Profile.get_absolute_url(self.object)


class ChangingUserPasswordView(PasswordChangeView):
    form_class = ChangingUserPasswordForm
    success_url = 'password_done'


@login_required(login_url='/login')
def password_change_done(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.user == user:
        logout(request)
        return redirect('authorisation_page')
    return redirect('main')


# @login_required(login_url='/login')
# def my_profile_page(request):
#     user = get_object_or_404(User, id=request.user.id)
#     if request.user == user:
#         profile_context = Profile.objects.select_related().filter(id=request.user.id)
#         return render(request, "my_profile/my_profile_page.html", {
#             'title': 'my_profile',
#             'profile_context': profile_context,
#         })
#     else:
#         return redirect("main")


@login_required(login_url='/login')
def profile_delete(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.user == user:
        logout(request)
        user.delete()
        return redirect("registration_page")
    else:
        return redirect("main")
