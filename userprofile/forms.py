from django.forms import EmailField
from django import forms

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True,
        help_text=_("Required."))
    is_vendor = forms.BooleanField(label=_("Are you a vendor?"), required=False)


    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2","is_vendor")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_vendor=self.cleaned_data["is_vendor"]
        if commit:
            user.save()
        return user