
from django.shortcuts import render,redirect
from .models import *
from django.db.models import Q
from django.http import HttpResponse,HttpResponseRedirect
from datetime import date,datetime
from django.db.models import Max
from decimal import Decimal
from django.http import JsonResponse
from django.db.models import Avg
from django.template.loader import get_template
from django.db.models import Count
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from .forms import CreateUserForms
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import datetime



def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForms()
        if request.method == "POST":
            form = CreateUserForms(request.POST)
            if form.is_valid():
                form.save()
                url = reverse('Auth:login') 
                return redirect(url)
        else:
          
            for field, errors in form.errors.items():
                for error in errors:
                   
                    if field == 'password2' and 'password1' in errors:
                        continue
                    messages.error(request, f"{field}: {error}")
        context = {'form': form}
        return render(request, 'auth/user_register.html', context)




def loginPage(request):
    if request.user.is_authenticated:
      return redirect('home')
    else:  

     if request.method == "POST":
      username =  request.POST.get('username')
      password =  request.POST.get('password')

      user=authenticate(request,   username=username,    password=password)

      if user is not None:
         request.session['username'] = username
         login(request,user)
         url = reverse('todo:home')

         return redirect(url)
      else:
         messages.info(request,'Username Or Password Is Incorrect')
         

     
    return render(request,'auth/user_login.html')






def LogoutPage(request):
   logout(request)
   return redirect('login')

