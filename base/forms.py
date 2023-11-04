from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, EmailField, CharField, PasswordInput, ImageField, Textarea

from base.models import Profile


class RegisterForm(UserCreationForm):
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    full_name = CharField(max_length=150, required=False)
    prof_pic = ImageField(required=False)
    location = CharField(max_length=150, required=False)
    bio = CharField(max_length=10000, required=False, widget=Textarea())

    class Meta:
        model = Profile
        fields = ['full_name', 'prof_pic', 'location', 'bio']
