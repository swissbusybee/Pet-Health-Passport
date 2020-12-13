from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm
from django.contrib.auth import forms as auth_forms

class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
      model = User
      fields = ['username', 'email', 'first_name', 'last_name']

class UserChangeForm(forms.ModelForm):

  class Meta:
      model = User
      fields = ['username', 'first_name', 'last_name', 'email',]