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

    password2 = forms.CharField(
        required=False, widget=forms.PasswordInput(),
        label='Confirmação senha')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password', 'password2')

    def clean(self):
        cleaned_data = self.cleaned_data
        validation_error_msgs = {}

        user_data = cleaned_data.get('username')
        email_data = cleaned_data.get('email')
        password_data = cleaned_data.get('password')
        password2_data = cleaned_data.get('password2')

        user_db = User.objects.filter(username=user_data).exclude(
            pk=self.user.pk if self.user else None).first()
        email_db = User.objects.filter(email=email_data).exclude(
            pk=self.user.pk if self.user else None).first()

        error_msg_user_exists = 'Usuário já existe.'
        error_email_exists = 'Email já existe.'
        error_password_match = 'As senhas são diferentes.'
        error_short_password = 'A senha deve ter mais que 6 caracteres.'
        error_required_field = 'Este campo é obrigatório.'

        if user_db:
            validation_error_msgs['username'] = error_msg_user_exists

        if email_db:
            validation_error_msgs['email'] = error_email_exists

        if password_data or password2_data:
            if password_data != password2_data:
                validation_error_msgs['password'] = error_password_match
                validation_error_msgs['password2'] = error_password_match
            if password_data and len(password_data) < 7:
                validation_error_msgs['password'] = error_short_password

        else:
            if not self.user:
                validation_error_msgs['password'] = error_required_field
                validation_error_msgs['password2'] = error_required_field

        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)

        return cleaned_data
