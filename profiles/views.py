# pylint: disable=all
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from . import models, forms
import copy


class ProfileBase(View):

    template_name = 'profiles/create.html'

    profile = None

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        if self.request.user.is_authenticated:
            self.profile = models.ProfileUser.objects.filter(
                user=self.request.user).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user, instance=self.request.user),

                'profileform': forms.ProfileForm(
                    data=self.request.POST or None),
                'title': 'Profile '

            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None),
                'title': 'Profile '

            }

        self.renderization = render(
            self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):

        return self.renderization


class Create(ProfileBase):
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        if self.request.user.is_authenticated:

            self.profile = models.ProfileUser.objects.filter(
                user=self.request.user).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user
                ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile
                )
            }
        else:

            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None),

            }

        if self.request.user.is_authenticated:
            self.template_name = 'profiles/update.html'

        self.renderization = render(
            self.request, self.template_name, self.context)

    def post(self, *args, **kwargs):
        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if not self.userform.is_valid() or not self.profileform.is_valid():
            return self.renderization

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            user = self.request.user
            user.username = username  # type: ignore

            if password:
                user.set_password(password)

            user.email = email  # type: ignore
            user.first_name = first_name  # type: ignore
            user.last_name = last_name  # type: ignore
            user.save()

            profile = models.ProfileUser.objects.filter(user=user).first()
            if profile:
                self.profileform = forms.ProfileForm(
                    data=self.request.POST, instance=profile
                )
                if self.profileform.is_valid():
                    self.profileform.save()
            else:
                profile = self.profileform.save(commit=False)
                profile.user = user
                profile.save()

        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()

        if password:
            auth = authenticate(
                self.request, username=user, password=password
            )
            if auth:
                login(self.request, user=user)  # type: ignore

        self.request.session['cart'] = self.cart
        self.request.session.save()
        return self.renderization


class Update(ProfileBase):
    def get(self, *args, **kwargs):
        return HttpResponse('Update')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
