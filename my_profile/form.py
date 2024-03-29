from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from registration_authorisation.models import User
from django import forms

from my_profile.models import Profile


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name'
        ]


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone', 'birthday', 'bio', 'email_subscribe', 'photo'
        ]


class ChangingUserPasswordForm(PasswordChangeForm):
    class META:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class ResetUserPasswordForm(PasswordResetForm):
    class META:
        model = User
        fields = ('new_password1', 'new_password2')
