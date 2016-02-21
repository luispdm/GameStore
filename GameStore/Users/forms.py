import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
"""
Django cleaning call stack
-> clean_<fieldname>()  : used to check validity of the file itself
-> clean()              : used to check validity over multiple fields
-> validate_unique()    : used to check validity of the whole object
"""


class RegistrationForm(UserCreationForm):
    username = forms.CharField(required=True, min_length=4, max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Bob'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'my@email.com'}))
    password1 = forms.CharField(required=True, min_length=8, max_length=30, label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, label="Confirm", widget=forms.PasswordInput())
    applyAsDeveloper = forms.NullBooleanField(label="Apply as Developer", widget=forms.CheckboxInput())

    def clean(self):
        # Clean is invoked after clean of each field. Here we take a chance to check for email uniqueness
        # Invoke basic clean system
        super(UserCreationForm, self).clean()

        # Custom checks for email uniqueness
        if User.objects.filter(email=self.cleaned_data.get('email')).count() > 0:
            raise ValidationError("E-mail already registered")

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')