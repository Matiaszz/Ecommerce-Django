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
        required=False, widget=forms.PasswordInput, label='Confirmação senha')

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password', 'password2')

    def clean(self):
        # data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        user_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe.'
        error_email_exists = 'Email já existe.'
        error_password_match = 'As senhas são diferentes.'
        error_short_password = 'A senha deve ter mais que 6 caracteres.'
        error_required_field = 'Este campo é obrigatório.'

        # user authenticated
        # if user authenticated, update the infos
        if self.user:
            if (user_db) and (user_data != user_db.username):
                validation_error_msgs['username'] = error_msg_user_exists

            if (email_db) and (email_data != email_db.email):
                validation_error_msgs['email'] = error_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_password_match
                    validation_error_msgs['password2'] = error_password_match

                if len(password_data) < 7:
                    validation_error_msgs['password'] = error_short_password

        # user not authenticated
        # else, register
        else:
            if (user_db) and (user_data == user_db.username):
                validation_error_msgs['username'] = error_msg_user_exists

            if (email_db) and (email_data != email_db.email):

                validation_error_msgs['email'] = error_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_password_match
                    validation_error_msgs['password2'] = error_password_match

                if len(password_data) < 7:
                    validation_error_msgs['password'] = error_short_password

            if not password_data:
                validation_error_msgs['password'] = error_required_field

            if not password2_data:
                validation_error_msgs['password2'] = error_required_field

        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)
