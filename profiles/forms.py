from django import forms
from . import models
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.ProfileUser
        fields = '__all__'
        exclude = ('user',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False, widget=forms.PasswordInput(), label='Senha')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def clean(self):
        data = self.data
        clean = self.cleaned_data
