# pylint: disable=all
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from . import models, forms


class ProfileBase(View):

    template_name = 'profiles/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        if self.request.user.is_authenticated:

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user, instance=self.request.user),

                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,),

            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None),

            }

        self.renderization = render(
            self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.renderization


class Create(ProfileBase):
    def post(self, *args, **kwargs):
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
