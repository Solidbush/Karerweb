from django import forms
from django.contrib.admin.forms import \
    AdminAuthenticationForm as _AdminAuthenticationForm
from django.utils.translation import gettext_lazy as _

from .models import Organization, User


class OrganizationCreateForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['inn', 'bik', 'phone']


class InviteDashboardForm(forms.Form):
    period = forms.ChoiceField(choices=[
        ('day', 'По дням'),
        ('week', 'По неделям'),
        ('month', 'По месячам'),
        ('quarter', "По квартал"),
        ('year', 'По годом'),
    ], label='Период')


class SendPvcForm(_AdminAuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(attrs={"autofocus": True}))
    password = None

    def clean(self):
        return self.cleaned_data


class AdminAuthenticationForm(_AdminAuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput())
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "autofocus": True}),
    )


class RegisterSendPvcForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "placeholder": "Адрес электронной почты",
        "style": "width: 100%; margin-top: 10px"
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "placeholder": "Имя",
        "style": "width: 100%; margin-top: 10px"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "autofocus": True,
        "placeholder": "Фамилия",
        "style": "width: 100%; margin-top: 10px"
    }))

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
