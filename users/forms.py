from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from users.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='usuario')
    pwd = forms.CharField(label='contraseña', widget=forms.PasswordInput())


class SignupForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
        }
        help_texts = {
            'username': ''
        }


class BlogForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('blog_name', 'visible_blog')
