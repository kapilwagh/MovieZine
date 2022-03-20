from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields
from django.db.models.fields.files import ImageField
from django.forms import widgets
from django import forms
from django.forms.widgets import ClearableFileInput, FileInput, PasswordInput, TextInput, NumberInput, EmailInput, URLInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Contact

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'john123'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'John'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Doe'}),
            'email': EmailInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'john@email.com'}),
            'password1': PasswordInput(attrs={'class': 'form-control', 'required': True}),
            'password2': PasswordInput(attrs={'class': 'form-control', 'required': True})
        }


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['full_name', 'email_id', 'message']
        widgets = {
            'full_name': TextInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Your Full Name'}),
            'email_id': EmailInput(attrs={'class': 'form-control', 'required': True, 'placeholder': 'Your Email-Id'}),
            'message': TextInput(attrs={'class': 'form-control', 'required': True, 'rows': '15', 'placeholder': 'Enter message...'})
        }