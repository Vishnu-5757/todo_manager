from django.forms import ModelForm
# from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django import forms
from  django.contrib.auth.models import User



class CreateUserForms(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
    
    