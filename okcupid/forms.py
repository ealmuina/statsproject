from django import forms
from django.contrib.auth.models import User

from okcupid.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    # TODO: LLenar con los datos especificos

    class Meta:
        model = UserProfile
        fields = ()
