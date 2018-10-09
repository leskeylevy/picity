from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image,Profile


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields =('username', 'email', 'password1', 'password2')


class PostImage(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image','caption')


class Prof(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('dp', 'bio')


